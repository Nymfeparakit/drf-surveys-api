from django.db import models


class Survey(models.Model):
    """
    Модель опроса
    """
    title = models.CharField(max_length=250)
    start_date = models.DateField() # дата начала
    end_date = models.DateField() # дата конца
    description = models.TextField(blank=True, null=True)

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
    survey_id = models.ForeignKey(
        'Survey',
        on_delete=models.CASCADE,
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
    question_id = models.ForeignKey(
        'Question',
        on_delete=models.CASCADE
    )
    text = models.CharField(max_length=250)
    number = models.IntegerField() # порядковый номер варианта ответа на вопрос

    class Meta:
        ordering = ['number']

    def __str__(self):
        return str(self.id)


class UserAnswersQuestion(models.Model):
    """
    Содержит информацию о выбранных пользователем вариантах ответа 
    Или написанном тексте ответа
    """
    user_id = models.ForeignKey(
        'SimpleUser',
        on_delete=models.CASCADE
    )
    question_id = models.ForeignKey(
        'Question',
        on_delete=models.CASCADE
    )
    choice_id = models.ForeignKey(
        'QuestionChoice',
        on_delete=models.CASCADE
    ) # выбранный ответ, если вопроса содержал варианты ответа
    answer_text = models.TextField() # текст ответа, если для вопроса не было вариантов ответа


class SimpleUser(models.Model):
    """
    Класс "пользователя", проходившего опрос
    Не содержит регистрации/авторизации, нужен только для хранения id анонимых пользователей, проходивших опросы
    """
    pass
