from django.db import models
from django.contrib.auth.models import User


class Instructor(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    full_time = models.BooleanField(default=True)
    total_learners = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class Learner(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    STUDENT = "student"
    DEVELOPER = "developer"
    DATA_SCIENTIST = "data_scientist"
    DATABASE_ADMIN = "dba"

    OCCUPATION_CHOICES = [
        (STUDENT, "Student"),
        (DEVELOPER, "Developer"),
        (DATA_SCIENTIST, "Data Scientist"),
        (DATABASE_ADMIN, "Database Admin"),
    ]

    occupation = models.CharField(
        max_length=20,
        choices=OCCUPATION_CHOICES,
        default=STUDENT
    )

    social_link = models.URLField(
        max_length=200,
        blank=True
    )

    def __str__(self):
        return self.user.username + "," + self.occupation


class Course(models.Model):
    name = models.CharField(
        max_length=30,
        default="online course"
    )
    description = models.CharField(
        max_length=1000,
        blank=True
    )
    pub_date = models.DateField(
        null=True,
        blank=True
    )
    instructors = models.ManyToManyField(
        Instructor,
        blank=True
    )
    total_enrollment = models.IntegerField(
        default=0
    )

    def __str__(self):
        return self.name


class Lesson(models.Model):
    title = models.CharField(
        max_length=200,
        default="title"
    )
    order = models.IntegerField(
        default=0
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE
    )
    content = models.TextField(
        blank=True
    )

    def __str__(self):
        return self.title


class Enrollment(models.Model):
    AUDIT = "audit"
    HONOR = "honor"
    BETA = "BETA"

    COURSE_MODES = [
        (AUDIT, "Audit"),
        (HONOR, "Honor"),
        (BETA, "BETA"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE
    )
    date_enrolled = models.DateField(
        auto_now_add=True
    )
    mode = models.CharField(
        max_length=5,
        choices=COURSE_MODES,
        default=AUDIT
    )
    rating = models.FloatField(
        default=5.0
    )

    def __str__(self):
        return f"{self.user.username} - {self.course.name}"


class Question(models.Model):
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    question_text = models.CharField(
        max_length=200
    )

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )
    choice_text = models.CharField(
        max_length=200
    )
    is_correct = models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.choice_text


class Submission(models.Model):
    enrollment = models.ForeignKey(
        Enrollment,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    choices = models.ManyToManyField(
        Choice
    )
    submitted_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Submission {self.id}"