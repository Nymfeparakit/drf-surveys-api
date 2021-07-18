import datetime
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, SAFE_METHODS, BasePermission
from datetime import date
from rest_framework import views
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework import status

from .models import Survey, Question, SimpleUser, UserAnswersQuestion, QuestionChoice
from .serializers import SurveySerializer, QuestionSerializer, UserTakesSurveySerializer, \
    SimpleUserSerializer, UserSurveysSerializer, UpdateSurveySerializer, QuestionChoiceSerializer


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class SurveyViewSet(viewsets.ModelViewSet):
    # serializer_class = SurveySerializer
    permission_classes = [IsAdminUser|ReadOnly]

    def get_queryset(self):
        """
        Возвращает queryset для объектов опроса
        Администраторы видят все объекты опросов
        Остальные пользователи видят только активные (с актуальной датой окончания)
        """
        qs = Survey.objects.all()
        if self.request.user.is_superuser:
            return qs
        return qs.filter(end_date__gte=date.today())

    def get_serializer_class(self):
        if self.action == 'partial_update' or self.action == 'update':
            return UpdateSurveySerializer
        else:
            return SurveySerializer


class QuesionChoiceViewSet(viewsets.ModelViewSet):
    """
    Создание/изменение/удаление вариантов ответа
    """
    serializer_class = QuestionChoiceSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return QuestionChoice.objects.filter(question=self.kwargs['question_pk'])


class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return Question.objects.filter(survey=self.kwargs['survey_pk'])


class TakeSurveyView(views.APIView):
    """
    Прохождение опроса
    """
    def post(self, request, format=None):
        data = request.data
        user_id = data['user_id']
        user = SimpleUser.objects.get_or_create(pk=user_id)
        serializer = UserTakesSurveySerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors)
        serializer.save()
        
        return Response(
            'Опрос успешно пройден',
            status=status.HTTP_200_OK
        )


class SimpleUserView(viewsets.ModelViewSet):
    queryset = SimpleUser.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = SimpleUserSerializer

    @action(detail=True, methods=['GET'])
    def surveys(self, request, pk=None):
        """
        Получение информации о пройденных пользователем опросах
        """
        user = get_object_or_404(SimpleUser, pk=pk)
        serializer = UserSurveysSerializer(user)
        return Response(serializer.data)