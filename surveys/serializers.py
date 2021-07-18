from rest_framework import serializers

from .models import Survey, Question, QuestionChoice, UserAnswersQuestion, UserTakesSurvey, SimpleUser


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SimpleUser
        fields = ['id']


class QuestionChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionChoice
        fields = ['text', 'number']

    def create(self, validated_data):
        question = Question.objects.get(pk=self.context["view"].kwargs["question_pk"])
        validated_data["question"] = question
        return Question.objects.create(**validated_data)


class QuestionSerializer(serializers.ModelSerializer):
    choices = QuestionChoiceSerializer(many=True, read_only=True)
    class Meta:
        model = Question
        fields = ['id', 'title', 'type', 'choices', 'number']
    
    def create(self, validated_data):
        survey = Survey.objects.get(pk=self.context["view"].kwargs["survey_pk"])
        validated_data["survey"] = survey
        return Question.objects.create(**validated_data)


class SurveySerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    class Meta:
        model = Survey
        fields = ['id', 'title', 'end_date', 'start_date', 'description', 'questions']


class UpdateSurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = ['id', 'title', 'start_date', 'end_date', 'description']
        read_only_fields = ['start_date']


class UserAnswersQuestionSerializer(serializers.ModelSerializer):
    choice = QuestionChoiceSerializer(read_only=True)
    class Meta:
        model = UserAnswersQuestion
        fields = ['question_id', 'choice', 'answer_text']


class UserAnswersQuestionListSerializer(serializers.BaseSerializer):
    def to_internal_value(self, data):
        return data

    def create(self, validated_data):
        user_survey_id = validated_data['user_survey_id']
        answers = validated_data['answers']
        answers_objs = []
        for answer in answers:
            if 'choices' in answer:
                for choice in answer['choices']:
                    answers_objs.append(UserAnswersQuestion(
                        user_survey_id=user_survey_id,
                        question_id=answer['question_id'],
                        choice_id=choice['choice_id']
                    ))
            else:
                answers_objs.append(UserAnswersQuestion(
                        user_survey_id=user_survey_id,
                        question_id=answer['question_id'],
                        answer_text=answer['answer_text']
                    ))
        return UserAnswersQuestion.objects.bulk_create(answers_objs)


class UserTakesSurveySerializer(serializers.ModelSerializer):
    answers = UserAnswersQuestionSerializer(many=True, read_only=True)
    class Meta:
        model = UserTakesSurvey
        fields = ['user_id', 'survey_id', 'answers']

    def to_internal_value(self, data):
        answers = data.get('answers')
        user_id = data.get('user_id')
        survey_id = data.get('survey_id')

        if not answers:
            raise serializers.ValidationError({
                'answers': 'This field is required.'
            })
        if not user_id:
            raise serializers.ValidationError({
                'user_id': 'This field is required.'
            })
        if not survey_id:
            raise serializers.ValidationError({
                'survey_id': 'This field is required.'
            })

        return {
            'user_id': int(user_id),
            'survey_id': int(survey_id),
            'answers': answers
        }

    def create(self, validated_data):
        user_takes_survey_obj = UserTakesSurvey.objects.create(
            user_id=validated_data['user_id'],
            survey_id=validated_data['survey_id']
        )
        answers_serializer = UserAnswersQuestionListSerializer(data={
            'user_survey_id': user_takes_survey_obj.id,
            'answers': validated_data['answers']
        })
        if not answers_serializer.is_valid():
            raise serializers.ValidationError(answers_serializer.errors)
        answers_serializer.save()
        return user_takes_survey_obj


class UserSurveysSerializer(serializers.ModelSerializer):
    surveys = UserTakesSurveySerializer(many=True, read_only=True)
    class Meta:
        model = SimpleUser
        fields = ('id', 'surveys')
