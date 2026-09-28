from django.shortcuts import render, redirect, get_object_or_404
from .models import Question, Choice, Submission


def exam(request):
    questions = Question.objects.prefetch_related("choice_set").all()

    return render(
        request,
        "onlinecourseapp/exam.html",
        {
            "questions": questions
        }
    )


def submit(request):
    if request.method == "POST":
        questions = Question.objects.prefetch_related("choice_set").all()
        score = 0

        for question in questions:
            selected_id = request.POST.get(f"question_{question.id}")

            if selected_id:
                choice = get_object_or_404(
                    Choice,
                    id=selected_id,
                    question=question
                )

                Submission.objects.create(
                    question=question,
                    selected_choice=choice
                )

                if choice.is_correct:
                    score += 1

        request.session["score"] = score
        request.session["total"] = questions.count()

        return redirect("show_exam_result")

    return redirect("exam")


def show_exam_result(request):
    score = request.session.get("score", 0)
    total = request.session.get("total", 0)

    return render(
        request,
        "onlinecourseapp/exam_result.html",
        {
            "score": score,
            "total": total,
        }
    )