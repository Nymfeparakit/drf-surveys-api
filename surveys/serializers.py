from rest_framework import serializers
from django.db.models import Count

from .models import Survey, Question, QuestionChoice, UserAnswersQuestion, UserTakesSurvey, SimpleUser


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SimpleUser
        fields = ['id']


class QuestionChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionChoice
        fields = ['id', 'text', 'number']

    def create(self, validated_data):
        """
        Создает вариант ответа
        Перед этим делает проверку, что вопрос не имеет текстовый тип
        """
        question = Question.objects\
        .annotate(choices_num=Count('choices'))\
        .get(pk=self.context["view"].kwargs["question_pk"])
        if question.type == 'text':
            raise serializers.ValidationError('Вопрос не может иметь вариантов ответа')
        validated_data["question"] = question
        return QuestionChoice.objects.create(**validated_data)


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
    """
    Сериализатор, используемый для обновления опроса
    Не позволяет изменить дату начала опроса
    """
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
    """
    Сериализует список ответов пользователя на вопросы
    """
    def to_internal_value(self, data):
        return data

    def create(self, validated_data):
        user_survey_id = validated_data['user_survey_id']
        user_takes_survey_obj = UserTakesSurvey.objects.select_related('survey').get(pk=user_survey_id)
        questions = Question.objects.select_related().prefetch_related('choices').filter(survey=user_takes_survey_obj.survey.id)
        questions_ids = questions.values_list('id')
        question_choices = QuestionChoice.objects.select_related().filter(question__in=questions_ids)
        answers = validated_data['answers']
        answers_objs = []

        for question in questions:
            answer = list(filter(lambda answer: answer['question_id'] == question.id, answers))
            if not answer:
                raise serializers.ValidationError(f'Нет ответа на вопрос {question.id}')
            answer = answer[0]
            if question.type == 'text':
                if 'answer_text' not in answer:
                    raise serializers.ValidationError(f'Нет ответа на вопрос {question.id}')
                answer_text = answer['answer_text']
                answers_objs.append(UserAnswersQuestion(
                        user_survey_id=user_survey_id,
                        question_id=answer['question_id'],
                        answer_text=answer_text
                    ))
            elif question.type == 'single_choice':
                if 'choice' not in answer:
                    raise serializers.ValidationError(f'Нет ответа на вопрос {question.id}')
                choice_id = answer['choice']
                if choice_id not in list(question.choices.values_list('id', flat=True)):
                    raise serializers.ValidationError(f'Некорректный ответ на вопрос {question.id}')
                answers_objs.append(UserAnswersQuestion(
                    user_survey_id=user_survey_id,
                    question_id=answer['question_id'],
                    choice_id=choice_id
                ))
            else:
                if 'choices' not in answer:
                        raise serializers.ValidationError(f'Нет ответа на вопрос {question.id}')
                choices_ids = answer['choices']
                possible_choices_ids = list(question.choices.values_list('id', flat=True))
                print('possible choices:', possible_choices_ids)
                for choice_id in choices_ids:
                    if choice_id not in possible_choices_ids:
                        raise serializers.ValidationError(f'Некорректный ответ на вопрос {question.id}')
                    answers_objs.append(UserAnswersQuestion(
                        user_survey_id=user_survey_id,
                        question_id=answer['question_id'],
                        choice_id=choice_id
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
