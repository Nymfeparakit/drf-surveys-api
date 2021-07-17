from rest_framework import serializers

from .models import Survey, Question, QuestionChoice


class QuestionChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionChoice
        fields = ['text', 'question_id']


class QuestionSerializer(serializers.ModelSerializer):
    choices = QuestionChoiceSerializer(many=True, read_only=True)
    class Meta:
        model = Question
        fields = ['id', 'title', 'type', 'survey_id', 'choices']


class SurveySerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    class Meta:
        model = Survey
        fields = ['id', 'title', 'start_date', 'end_date', 'description', 'questions']
