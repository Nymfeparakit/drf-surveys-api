from django.contrib import admin

from .models import Survey, Question, QuestionChoice, UserTakesSurvey, UserAnswersQuestion, SimpleUser


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    pass


class QuestionChoiceInline(admin.TabularInline):
    model = QuestionChoice


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [QuestionChoiceInline,]


@admin.register(UserAnswersQuestion)
class UserAnswersQuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(UserTakesSurvey)
class UserTakesSurveyAdmin(admin.ModelAdmin):
    pass


@admin.register(SimpleUser)
class SimpleUserAdmin(admin.ModelAdmin):
    list_display = ('id',)