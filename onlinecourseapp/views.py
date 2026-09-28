from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Question, Choice, Submission, Course, Enrollment


def exam(request):
    questions = Question.objects.prefetch_related("choice_set").all()

    return render(
        request,
        "onlinecourseapp/exam.html",
        {"questions": questions}
    )


def submit(request, course_id):
    if request.method == "POST":

        questions = Question.objects.prefetch_related("choice_set").all()

        # Get or create the course
        course, created = Course.objects.get_or_create(
            id=course_id,
            defaults={"name": "Online Course Mock Exam"}
        )

        # Use logged-in user, or first available user for mock exam
        if request.user.is_authenticated:
            user = request.user
        else:
            user = User.objects.first()

        # Create or get enrollment
        enrollment, created = Enrollment.objects.get_or_create(
            user=user,
            course=course,
            defaults={"mode": Enrollment.AUDIT}
        )

        # Create one submission for the complete exam
        submission = Submission.objects.create(
            enrollment=enrollment
        )

        score = 0

        for question in questions:

            selected_id = request.POST.get(
                f"question_{question.id}"
            )

            if selected_id:

                choice = get_object_or_404(
                    Choice,
                    id=selected_id,
                    question=question
                )

                # Store selected choice in ManyToMany field
                submission.choices.add(choice)

                if choice.is_correct:
                    score += 1

        request.session["score"] = score
        request.session["total"] = questions.count()

        return redirect(
            "show_exam_result",
            course_id=course_id,
            submission_id=submission.id
        )

    return redirect("exam")


def show_exam_result(request, course_id, submission_id):

    get_object_or_404(
        Submission,
        id=submission_id
    )

    questions = Question.objects.prefetch_related(
        "choice_set"
    ).all()

    score = request.session.get("score", 0)

    total = request.session.get(
        "total",
        questions.count()
    )

    results = []

    for question in questions:

        correct_choice = question.choice_set.filter(
            is_correct=True
        ).first()

        results.append({
            "question": question,
            "correct_choice": correct_choice,
        })

    return render(
        request,
        "onlinecourseapp/exam_result.html",
        {
            "score": score,
            "total": total,
            "results": results,
        }
    )