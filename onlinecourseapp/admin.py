from django.contrib import admin
from .models import Question, Choice, Submission


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionInline(admin.StackedInline):
    model = Choice
    extra = 3


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["question_text"]}),
    ]
    inlines = [ChoiceInline]
    list_display = ["question_text"]


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ["question", "selected_choice", "submitted_at"]


class LessonAdmin(admin.ModelAdmin):
    list_display = ["id"]