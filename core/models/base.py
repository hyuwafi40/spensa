from django.db import models
from core.utils.constants import JournalActivityChoices, JournalModuleChoices
from core.utils.services import (
    generate_unique_slug,
    validate_student,
    validate_teacher,
    validate_time_range,
)


class TimeStampedMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SlugMixin(models.Model):
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(
                self.__class__, self.get_slug_source(), instance=self
            )
        super().save(*args, **kwargs)

    def get_slug_source(self):
        raise NotImplementedError("Subclass must implement get_slug_source()")


class TeacherValidationMixin:
    def clean(self):
        validate_teacher(self.teacher)
        super().clean()

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class StudentValidationMixin:
    def clean(self):
        validate_student(self.student)
        super().clean()

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class TimeRangeValidationMixin:
    def clean(self):
        validate_time_range(self.start_time, self.end_time)
        super().clean()


class BaseJournal(TimeStampedMixin):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Waktu Aktivitas")
    activity = models.CharField(max_length=20, choices=JournalActivityChoices.choices)
    module = models.CharField(max_length=50, choices=JournalModuleChoices.choices)
    target_name = models.CharField(max_length=255, blank=True)
    reference_id = models.PositiveBigIntegerField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["module", "activity"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"{self.get_activity_display()} - {self.get_module_display()} - {self.target_name}"
