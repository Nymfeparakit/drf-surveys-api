import datetime
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from datetime import date
from rest_framework import views
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework import status

from .models import Survey, Question, SimpleUser, UserAnswersQuestion
from .serializers import SurveySerializer, QuestionSerializer, UserTakesSurveySerializer, \
     SimpleUserSerializer, UserSurveysSerializer


class SurveyViewSet(viewsets.ModelViewSet):
    serializer_class = SurveySerializer

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


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAdminUser]


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
            'Survey was completed successfully',
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