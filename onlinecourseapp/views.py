from django.shortcuts import render, redirect, get_object_or_404
from .models import Question, Choice, Submission


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

        score = 0
        first_submission_id = None

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

                submission = Submission.objects.create(
                    question=question,
                    selected_choice=choice
                )

                if first_submission_id is None:
                    first_submission_id = submission.id

                if choice.is_correct:
                    score += 1

        request.session["score"] = score
        request.session["total"] = questions.count()

        if first_submission_id:
            return redirect(
                "show_exam_result",
                course_id=course_id,
                submission_id=first_submission_id
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