from django.apps import apps
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from core.utils.services import sync_username_from_profile


@receiver(post_save, sender=apps.get_model("core", "Profile"))
def sync_username(sender, instance, **kwargs):
    sync_username_from_profile(instance)


@receiver(
    [post_save, post_delete], sender=apps.get_model("core", "AssignmentSubmission")
)
def recalc_assessment_on_assignment_submission(sender, instance, **kwargs):
    Assessment = apps.get_model("core", "Assessment")
    assessments = Assessment.objects.filter(
        student=instance.student,
        subject=instance.assignment.subject,
        active_year__year=instance.assignment.academic_year,
        active_year__term=instance.assignment.term,
    )
    for assessment in assessments:
        assessment.save()


@receiver([post_save, post_delete], sender=apps.get_model("core", "QuizAttempt"))
def recalc_assessment_on_quiz_attempt(sender, instance, **kwargs):
    Assessment = apps.get_model("core", "Assessment")
    assessments = Assessment.objects.filter(
        student=instance.student,
        subject=instance.quiz.subject,
        active_year__year=instance.quiz.academic_year,
        active_year__term=instance.quiz.term,
    )
    for assessment in assessments:
        assessment.save()
