from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Course, Lesson, Question, Choice, Submission


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["question_text", "lesson"]}),
    ]
    inlines = [ChoiceInline]
    list_display = ["question_text", "lesson"]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ["name", "course"]
    inlines = [QuestionInline]


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ["question", "selected_choice", "submitted_at"]