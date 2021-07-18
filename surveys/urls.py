from django.db.models import base
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import SurveyViewSet, QuestionViewSet, TakeSurveyView, SimpleUserView


surveys_router = SimpleRouter()
surveys_router.register(r'surveys', SurveyViewSet, basename='surveys')
surveys_router.register(r'questions', QuestionViewSet, basename='questions')
surveys_router.register(r'users', SimpleUserView, basename='users')

urlpatterns = [
    path('', include(surveys_router.urls)),
    path('survey_takes', TakeSurveyView.as_view()),
]
