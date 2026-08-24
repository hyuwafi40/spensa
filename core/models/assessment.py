from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from core.models.account import CustomUser
from core.models.academic import ActiveYear, Subject
from core.models.base import TimeStampedMixin
from core.utils.calculations import calculate_daily_score, calculate_grade
from core.utils.constants import JobChoices
from core.utils.services import validate_student, validate_teacher


class Assessment(TimeStampedMixin):
    student = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={"job": JobChoices.STUDENT},
        related_name="assessments",
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.PROTECT,
        related_name="assessments",
    )
    active_year = models.ForeignKey(
        ActiveYear,
        on_delete=models.PROTECT,
        related_name="assessments",
    )
    teacher = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        limit_choices_to={"job": JobChoices.TEACHER},
        related_name="graded_assessments",
    )
    daily_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        editable=False,
    )
    midterm_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    final_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    total_score = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True, editable=False
    )
    grade_letter = models.CharField(max_length=2, blank=True, editable=False)

    def clean(self):
        validate_student(self.student)
        validate_teacher(self.teacher)

    def save(self, *args, **kwargs):
        self.clean()
        self.daily_score = calculate_daily_score(
            self.student,
            self.subject,
            self.active_year,
        )
        self.total_score, self.grade_letter = calculate_grade(
            self.daily_score,
            self.midterm_score,
            self.final_score,
        )
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Penilaian"
        verbose_name_plural = "Penilaian"
        constraints = [
            models.UniqueConstraint(
                fields=["student", "subject", "active_year"],
                name="unique_assessment",
            )
        ]

    def __str__(self):
        return f"{self.student.username} - {self.subject.name} - {self.active_year}"
