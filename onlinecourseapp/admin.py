from django.contrib import admin
from .models import (
    Instructor,
    Learner,
    Course,
    Lesson,
    Enrollment,
    Question,
    Choice,
    Submission,
)


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
    list_display = ["title", "course"]
    inlines = [QuestionInline]


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["name", "pub_date", "total_enrollment"]


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ["user", "full_time", "total_learners"]


@admin.register(Learner)
class LearnerAdmin(admin.ModelAdmin):
    list_display = ["user", "occupation"]


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ["user", "course", "date_enrolled", "mode", "rating"]


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ["choice_text", "question", "is_correct"]


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ["id", "enrollment", "submitted_at"]