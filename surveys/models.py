from django.db import models


class Survey(models.Model):
    """
    Модель опроса
    """
    title = models.CharField(max_length=250)
    start_date = models.DateField() # дата начала
    end_date = models.DateField() # дата конца
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    """
    Вопрос, содержащийся в опросе
    Содержит информацию о тексте вопроса, его типе
    """
    TYPE_CHOICES = (
        ('text', 'text'),
        ('single_choice', 'single_choice'),
        ('multiple_choice', 'multiple_choice'),
    )
    survey = models.ForeignKey(
        'Survey',
        on_delete=models.CASCADE,
        related_name='questions'
    )
    title = models.CharField(max_length=250)
    number = models.IntegerField() # порядковый номер вопроса в опросе
    type = models.CharField(
        max_length=15,
        choices=TYPE_CHOICES,
        default='text'
    )

    class Meta:
        ordering = ['number']

    def __str__(self):
        return self.title


class QuestionChoice(models.Model):
    """
    Вариант ответа на вопроса
    """
    question = models.ForeignKey(
        'Question',
        on_delete=models.CASCADE,
        related_name='choices'
    )
    text = models.CharField(max_length=250)
    number = models.IntegerField() # порядковый номер варианта ответа на вопрос

    class Meta:
        ordering = ['number']

    def __str__(self):
        return str(self.id)


class UserTakesSurvey(models.Model):
    """
    Опрос, пройденный пользователем
    """
    user = models.ForeignKey(
        'SimpleUser',
        on_delete=models.CASCADE,
        related_name='surveys'
    )
    survey = models.ForeignKey(
        'Survey',
        on_delete=models.CASCADE,
        related_name='survey_obj'
    )


class UserAnswersQuestion(models.Model):
    """
    Содержит информацию о выбранных пользователем вариантах ответа 
    Или написанном тексте ответа
    """
    user_survey = models.ForeignKey(
        'UserTakesSurvey',
        on_delete=models.CASCADE,
        related_name='answers'
    )
    question = models.ForeignKey(
        'Question',
        on_delete=models.CASCADE,
        related_name='answer'
    )
    choice = models.ForeignKey(
        'QuestionChoice',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    ) # выбранный ответ, если вопроса содержал варианты ответа
    answer_text = models.TextField(blank=True) # текст ответа, если для вопроса не было вариантов ответа


class SimpleUser(models.Model):
    """
    Класс "пользователя", проходившего опрос
    Не содержит регистрации/авторизации, нужен только для хранения id анонимых пользователей, проходивших опросы
    """
    pass
