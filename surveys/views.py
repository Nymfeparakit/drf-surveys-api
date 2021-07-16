import datetime
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from datetime import date

from .models import Survey, Question
from .serializers import SurveySerializer, QuestionSerializer


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
