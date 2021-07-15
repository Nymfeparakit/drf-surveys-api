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
    survey_id = models.ForeignKey()
    title = models.CharField(max_length=250)
    type = models.CharField(
        max_length=15,
        choices=TYPE_CHOICES,
        default='text'
    )