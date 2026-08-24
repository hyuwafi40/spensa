import math
from decimal import Decimal
from django.db.models import Avg


def calculate_grade(daily_score, midterm_score, final_score):
    try:
        daily = float(daily_score or 0)
        mid = float(midterm_score or 0)
        final = float(final_score or 0)
    except (TypeError, ValueError):
        return None, ""
    total = daily * 0.4 + mid * 0.3 + final * 0.3
    total = round(total, 2)
    if total >= 90:
        letter = "A"
    elif total >= 80:
        letter = "B"
    elif total >= 70:
        letter = "C"
    elif total >= 60:
        letter = "D"
    else:
        letter = "E"
    return total, letter


def calculate_daily_score(student, subject, active_year):
    from core.models.learning import AssignmentSubmission, QuizAttempt

    assignment_avg = (
        AssignmentSubmission.objects.filter(
            assignment__subject=subject,
            assignment__academic_year=active_year.year,
            assignment__term=active_year.term,
            student=student,
            score__isnull=False,
        ).aggregate(avg=Avg("score"))["avg"]
        or 0
    )

    quiz_avg = (
        QuizAttempt.objects.filter(
            quiz__subject=subject,
            quiz__academic_year=active_year.year,
            quiz__term=active_year.term,
            student=student,
            score__isnull=False,
        ).aggregate(avg=Avg("score"))["avg"]
        or 0
    )

    daily = float(assignment_avg) * 0.6 + float(quiz_avg) * 0.4
    daily = math.ceil(daily * 100) / 100
    daily = min(daily, 100.0)
    return Decimal(str(daily))
