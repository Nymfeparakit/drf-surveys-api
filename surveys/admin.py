from django.contrib import admin

from .models import Survey, Question, QuestionChoice


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    pass


class QuestionChoiceInline(admin.TabularInline):
    model = QuestionChoice


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [QuestionChoiceInline,]
