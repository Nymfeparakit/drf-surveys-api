from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from .models import Survey, Question
from .serializers import SurveySerializer, QuestionSerializer


class SurveyViewSet(viewsets.ModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
