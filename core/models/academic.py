from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import (
    MinLengthValidator,
    MaxLengthValidator,
    MinValueValidator,
    MaxValueValidator,
)
from core.models.base import TimeStampedMixin
from core.models.account import CustomUser
from core.utils.constants import ClassLevelChoices, JobChoices, TermChoices
from core.utils.services import set_active_year, validate_student, validate_teacher
from core.utils.validators import validate_year


class Year(TimeStampedMixin):
    start_year = models.CharField(max_length=4, validators=[validate_year])
    finish_year = models.CharField(max_length=4, validators=[validate_year])

    class Meta:
        verbose_name = "Tahun Ajaran"
        verbose_name_plural = "Tahun Ajaran"
        unique_together = ("start_year", "finish_year")

    def __str__(self):
        return f"{self.start_year}/{self.finish_year}"


class Term(TimeStampedMixin):
    name = models.CharField(max_length=20, choices=TermChoices.choices, unique=True)

    class Meta:
        verbose_name = "Semester"
        verbose_name_plural = "Semester"

    def __str__(self):
        return self.get_name_display()


class Subject(TimeStampedMixin):
    code = models.CharField(
        max_length=6,
        validators=[MinLengthValidator(3), MaxLengthValidator(6)],
        unique=True,
    )
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Mata Pelajaran"
        verbose_name_plural = "Mata Pelajaran"

    def __str__(self):
        return f"{self.code} - {self.name}"


class Classroom(TimeStampedMixin):
    grade = models.CharField(max_length=2, choices=ClassLevelChoices.choices)
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Ruang Belajar"
        verbose_name_plural = "Ruang Belajar"
        unique_together = ("grade", "name")

    def __str__(self):
        return f"Kelas {self.grade} - {self.name}"


class ActiveYear(TimeStampedMixin):
    year = models.ForeignKey(
        Year,
        on_delete=models.PROTECT,
        related_name="active_years",
    )
    term = models.ForeignKey(
        Term,
        on_delete=models.PROTECT,
        related_name="active_years",
    )
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Tahun Ajaran Aktif"
        verbose_name_plural = "Tahun Ajaran Aktif"
        unique_together = ("year", "term")

    def save(self, *args, **kwargs):
        if self.is_active:
            set_active_year(self)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.year} - {self.term}"


class ActiveSubject(TimeStampedMixin):
    active_year = models.ForeignKey(
        ActiveYear,
        on_delete=models.PROTECT,
        related_name="active_subjects",
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.PROTECT,
        related_name="active_subjects",
    )
    classroom = models.ForeignKey(
        Classroom,
        on_delete=models.PROTECT,
        related_name="active_subjects",
    )
    teacher = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        limit_choices_to={"job": JobChoices.TEACHER},
        related_name="active_subjects",
    )

    class Meta:
        verbose_name = "Mata Pelajaran Aktif"
        verbose_name_plural = "Mata Pelajaran Aktif"
        unique_together = ("active_year", "subject", "classroom", "teacher")

    def clean(self):
        validate_teacher(self.teacher)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.active_year} - {self.subject.name} - {self.classroom} - {self.teacher.username}"


class ActiveClassroom(TimeStampedMixin):
    active_year = models.ForeignKey(
        ActiveYear,
        on_delete=models.PROTECT,
        related_name="active_classrooms",
    )
    classroom = models.ForeignKey(
        Classroom,
        on_delete=models.PROTECT,
        related_name="active_classrooms",
    )
    teacher = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        limit_choices_to={"job": JobChoices.TEACHER},
        related_name="active_classrooms",
    )
    quota = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(35)],
    )

    class Meta:
        verbose_name = "Ruang Belajar Aktif"
        verbose_name_plural = "Ruang Belajar Aktif"
        unique_together = ("active_year", "classroom")
        constraints = [
            models.UniqueConstraint(
                fields=["active_year", "teacher"],
                name="unique_teacher_active_classroom",
            ),
        ]

    def clean(self):
        validate_teacher(self.teacher)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.active_year} - {self.classroom} - {self.teacher.username}"


class ActiveStudent(TimeStampedMixin):
    classroom = models.ForeignKey(
        ActiveClassroom,
        on_delete=models.PROTECT,
        related_name="active_students",
    )
    student = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        limit_choices_to={"job": JobChoices.STUDENT},
        related_name="active_students",
    )
    active_year = models.ForeignKey(
        ActiveYear,
        on_delete=models.PROTECT,
        related_name="active_students",
        blank=True,
        null=True,
        editable=False,
    )

    class Meta:
        verbose_name = "Siswa Aktif"
        verbose_name_plural = "Siswa Aktif"
        constraints = [
            models.UniqueConstraint(
                fields=["student", "active_year"], name="unique_student_active_year"
            ),
        ]

    def clean(self):
        validate_student(self.student)
        if self.classroom_id:
            self.active_year = self.classroom.active_year
            if (
                self.classroom.quota > 0
                and self.classroom.active_students.count() >= self.classroom.quota
            ):
                if (
                    not self.pk
                    or self.classroom_id
                    != self.__class__.objects.filter(pk=self.pk)
                    .values_list("classroom_id", flat=True)
                    .first()
                ):
                    raise ValidationError("Kuota kelas sudah penuh.")

    def save(self, *args, **kwargs):
        if self.classroom_id:
            self.active_year = self.classroom.active_year
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.classroom} - {self.student.username}"
