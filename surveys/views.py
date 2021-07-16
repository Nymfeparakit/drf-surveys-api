from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from .models import Survey
from .serializers import SurveySerializer


class SurveyViewSet(viewsets.ModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
