from django.db import models
from core.models.account import CustomUser
from core.models.base import BaseJournal
from core.utils.constants import JobChoices
from core.utils.services import validate_student, validate_teacher


class TeacherJournal(BaseJournal):
    teacher = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        limit_choices_to={"job": JobChoices.TEACHER},
        related_name="teacher_journals",
    )

    def clean(self):
        validate_teacher(self.teacher)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Jurnal Guru"
        verbose_name_plural = "Jurnal Guru"

    def __str__(self):
        return f"{self.teacher.username} - {super().__str__()}"


class StudentJournal(BaseJournal):
    student = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        limit_choices_to={"job": JobChoices.STUDENT},
        related_name="student_journals",
    )

    def clean(self):
        validate_student(self.student)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Jurnal Siswa"
        verbose_name_plural = "Jurnal Siswa"

    def __str__(self):
        return f"{self.student.username} - {super().__str__()}"
