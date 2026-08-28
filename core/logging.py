from django.apps import apps
from django.db import transaction
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from core.middleware import get_current_user
from core.models.log import DeveloperLog
from core.utils.constants import JournalActivityChoices, LogLevelChoices

TRACKED_MODELS = [
    ("account", "CustomUser"),
    ("account", "Profile"),
    ("brand", "Brand"),
    ("brand", "School"),
    ("academic", "Year"),
    ("academic", "Term"),
    ("academic", "Subject"),
    ("academic", "Classroom"),
    ("academic", "ActiveYear"),
    ("academic", "ActiveSubject"),
    ("academic", "ActiveClassroom"),
    ("academic", "ActiveStudent"),
    ("learning", "Material"),
    ("learning", "Assignment"),
    ("learning", "AssignmentSubmission"),
    ("learning", "QuestionBank"),
    ("learning", "Question"),
    ("learning", "AnswerOption"),
    ("learning", "Quiz"),
    ("learning", "QuizAttempt"),
    ("assessment", "Assessment"),
    ("journal", "TeacherJournal"),
    ("journal", "StudentJournal"),
]


def get_module_for_model(model):
    return model.__name__.lower()


def log_model_activity(sender, instance, created=False, deleted=False):
    action = (
        JournalActivityChoices.DELETE
        if deleted
        else (
            JournalActivityChoices.CREATE if created else JournalActivityChoices.UPDATE
        )
    )
    module = get_module_for_model(sender)
    object_repr = str(instance)[:255] if instance else ""

    def create_log():
        DeveloperLog.objects.create(
            level=LogLevelChoices.INFO,
            event=f"{action} {module}",
            user=get_current_user(),
            module=module,
            object_id=instance.pk,
            action=action,
            object_repr=object_repr,
        )

    transaction.on_commit(create_log)


def register_signals():
    for app_label, model_name in TRACKED_MODELS:
        try:
            model = apps.get_model(app_label, model_name)
            post_save.connect(
                receiver(
                    lambda sender, instance, created, **kwargs: log_model_activity(
                        sender, instance, created=created
                    ),
                    weak=False,
                ),
                sender=model,
                dispatch_uid=f"{model_name}_save_log",
            )
            post_delete.connect(
                receiver(
                    lambda sender, instance, **kwargs: log_model_activity(
                        sender, instance, deleted=True
                    ),
                    weak=False,
                ),
                sender=model,
                dispatch_uid=f"{model_name}_delete_log",
            )
        except LookupError:
            continue
