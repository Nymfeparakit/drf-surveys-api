from django.db.models import base
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers

from .views import SurveyViewSet, QuestionViewSet, TakeSurveyView, SimpleUserView, QuesionChoiceViewSet


surveys_router = SimpleRouter()
surveys_router.register(r'surveys', SurveyViewSet, basename='surveys')

questions_router = routers.NestedSimpleRouter(surveys_router, r'surveys', lookup='survey')
questions_router.register(r'questions', QuestionViewSet, basename='questions')

choices_router = routers.NestedSimpleRouter(questions_router, r'questions', lookup='question')
choices_router.register(r'choices', QuesionChoiceViewSet, basename='choices')

users_router = SimpleRouter()
users_router.register(r'users', SimpleUserView, basename='users')

urlpatterns = [
    path('', include(surveys_router.urls)),
    path('', include(questions_router.urls)),
    path('', include(choices_router.urls)),
    path('', include(users_router.urls)),
    path('survey_takes', TakeSurveyView.as_view()),
]
