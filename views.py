from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import Course, Choice, Submission


def course_details(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    return render(
        request,
        "onlinecourse/course_details_bootstrap.html",
        {"course": course}
    )


@login_required
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    if request.method != "POST":
        return redirect(
            "onlinecourse:course_details",
            course_id=course.id
        )

    questions = course.questions.all()
    score = 0
    selected_choices = []

    for question in questions:
        selected_id = request.POST.get(
            f"question_{question.id}"
        )

        if not selected_id:
            continue

        choice = Choice.objects.filter(
            pk=selected_id,
            question=question
        ).first()

        if choice:
            selected_choices.append(choice)

            if choice.is_correct:
                score += question.grade

    submission = Submission.objects.create(
        user=request.user,
        course=course,
        score=score
    )

    submission.choices.set(selected_choices)

    return redirect(
        "onlinecourse:show_exam_result",
        submission_id=submission.id
    )


@login_required
def show_exam_result(request, submission_id):
    submission = get_object_or_404(
        Submission.objects.prefetch_related("choices"),
        pk=submission_id,
        user=request.user
    )

    total_score = sum(
        question.grade
        for question in submission.course.questions.all()
    )

    results = []

    for question in submission.course.questions.all():
        selected = submission.choices.filter(
            question=question
        ).first()

        correct = question.choices.filter(
            is_correct=True
        ).first()

        results.append({
            "question": question,
            "selected": selected,
            "correct": correct,
            "is_correct": bool(
                selected and selected.is_correct
            ),
        })

    return render(
        request,
        "onlinecourse/exam_result.html",
        {
            "submission": submission,
            "results": results,
            "total_score": total_score,
        }
    )


@require_POST
def logout_user(request):
    logout(request)

    return JsonResponse({
        "message": "Logout successful"
    })
