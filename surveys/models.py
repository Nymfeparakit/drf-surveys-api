from django.db import models


class Survey(models.Model):
    title = models.CharField(max_length=250)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    description = models.TextField()

    def __str__(self):
        return self.title


class Question(models.Model):
    TYPE_CHOICES = (
        ('text', 'text'),
        ('single_choice', 'single_choice'),
        ('multiple_choice', 'multiple_choice'),
    )
    survey_id = models.ForeignKey(
        'Syrvey',
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=250)
    type = models.CharField(
        max_length=15,
        choices=TYPE_CHOICES,
        default='text'
    )

    def __str__(self):
        return self.title


class QuestionChoice(models.Model):
    """
    Вариант ответа для вопроса
    """
    question_id = models.ForeignKey(
        'Question',
        on_delete=models.CASCADE
    )
    text = models.CharField(max_length=250)


class UserAnswersQuestion(models.Model):
    """
    Содержит информацию о выбранных пользователем вариантах ответа 
    Или написанном тексте ответа
    """
    user_id = models.IntegerField()
    question_id = models.ForeignKey(
        'Question',
        on_delete=models.CASCADE
    )
    choice_id = models.ForeignKey(
        'QuestionChoice',
        on_delete=models.CASCADE
    ) # выбранный ответ, если вопроса содержал варианты ответа
    answer_text = models.TextField() # текст ответа, если для вопроса не было вариантов ответа
