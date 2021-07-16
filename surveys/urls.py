from django.db.models import base
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import SurveyViewSet


surveys_router = SimpleRouter()
surveys_router.register(r'surveys', SurveyViewSet, basename='surveys')

urlpatterns = [
    path('', include(surveys_router.urls)),
]
