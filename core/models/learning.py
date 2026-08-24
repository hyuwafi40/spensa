from django.db import models
from core.models.account import CustomUser
from core.models.academic import Classroom, Subject, Term, Year
from core.models.base import (
    StudentValidationMixin,
    TeacherValidationMixin,
    TimeRangeValidationMixin,
    TimeStampedMixin,
)
from core.utils.constants import (
    AssignmentStatusChoices,
    AssignmentTypeChoices,
    DifficultyChoices,
    QuestionTypeChoices,
    QuizStatusChoices,
    SubmissionStatusChoices,
    TEACHER_LIMIT,
    STUDENT_LIMIT,
)


class Material(TeacherValidationMixin, TimeStampedMixin):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to="materials/%Y/%m/%d/")
    material_type = models.CharField(max_length=20, blank=True)
    subject = models.ForeignKey(
        Subject,
        on_delete=models.PROTECT,
        related_name="materials",
    )
    teacher = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        limit_choices_to=TEACHER_LIMIT,
        related_name="materials",
    )
    classroom = models.ForeignKey(
        Classroom,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="materials",
    )
    academic_year = models.ForeignKey(
        Year,
        on_delete=models.PROTECT,
        related_name="materials",
    )

    class Meta:
        verbose_name = "Materi Ajar"
        verbose_name_plural = "Materi Ajar"

    def __str__(self):
        return self.title


class Assignment(TeacherValidationMixin, TimeStampedMixin):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    type = models.CharField(max_length=20, choices=AssignmentTypeChoices.choices)
    subject = models.ForeignKey(
        Subject,
        on_delete=models.PROTECT,
        related_name="assignments",
    )
    teacher = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        limit_choices_to=TEACHER_LIMIT,
        related_name="assignments",
    )
    classroom = models.ForeignKey(
        Classroom,
        on_delete=models.PROTECT,
        related_name="assignments",
    )
    academic_year = models.ForeignKey(
        Year,
        on_delete=models.PROTECT,
        related_name="assignments",
    )
    term = models.ForeignKey(
        Term,
        on_delete=models.PROTECT,
        related_name="assignments",
    )
    due_date = models.DateTimeField(null=True, blank=True)
    max_score = models.DecimalField(max_digits=5, decimal_places=2, default=100.00)
    file_attachment = models.FileField(
        upload_to="assignments/%Y/%m/%d/", blank=True, null=True
    )
    status = models.CharField(
        max_length=20,
        choices=AssignmentStatusChoices.choices,
        default=AssignmentStatusChoices.DRAFT,
    )

    class Meta:
        verbose_name = "Tugas"
        verbose_name_plural = "Tugas"

    def __str__(self):
        return self.title


class AssignmentSubmission(StudentValidationMixin, TimeStampedMixin):
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name="submissions",
    )
    student = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to=STUDENT_LIMIT,
        related_name="assignment_submissions",
    )
    file_upload = models.FileField(
        upload_to="submissions/%Y/%m/%d/", blank=True, null=True
    )
    text_answer = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    feedback = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=SubmissionStatusChoices.choices,
        default=SubmissionStatusChoices.SUBMITTED,
    )

    class Meta:
        verbose_name = "Pengumpulan Tugas"
        verbose_name_plural = "Pengumpulan Tugas"
        constraints = [
            models.UniqueConstraint(
                fields=["assignment", "student"],
                name="unique_assignment_submission",
            )
        ]

    def __str__(self):
        return f"{self.assignment.title} - {self.student.username}"


class QuestionBank(TeacherValidationMixin, TimeStampedMixin):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    subject = models.ForeignKey(
        Subject,
        on_delete=models.PROTECT,
        related_name="question_banks",
    )
    teacher = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        limit_choices_to=TEACHER_LIMIT,
        related_name="question_banks",
    )
    is_public = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Bank Soal"
        verbose_name_plural = "Bank Soal"

    def __str__(self):
        return self.name


class Question(TeacherValidationMixin, TimeStampedMixin):
    question_bank = models.ForeignKey(
        QuestionBank,
        on_delete=models.CASCADE,
        related_name="questions",
        null=True,
        blank=True,
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.PROTECT,
        related_name="questions",
    )
    teacher = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        limit_choices_to=TEACHER_LIMIT,
        related_name="questions",
    )
    question_text = models.TextField()
    question_type = models.CharField(max_length=2, choices=QuestionTypeChoices.choices)
    difficulty = models.CharField(
        max_length=10,
        choices=DifficultyChoices.choices,
        default=DifficultyChoices.MEDIUM,
    )
    points = models.DecimalField(max_digits=5, decimal_places=2, default=1.00)

    class Meta:
        verbose_name = "Soal"
        verbose_name_plural = "Soal"

    def __str__(self):
        return self.question_text[:50]


class AnswerOption(TimeStampedMixin):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="answer_options",
    )
    text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = "Opsi Jawaban"
        verbose_name_plural = "Opsi Jawaban"

    def __str__(self):
        return f"{self.question.question_text[:30]} - {self.text[:30]}"


class Quiz(TeacherValidationMixin, TimeRangeValidationMixin, TimeStampedMixin):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    subject = models.ForeignKey(
        Subject,
        on_delete=models.PROTECT,
        related_name="quizzes",
    )
    teacher = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        limit_choices_to=TEACHER_LIMIT,
        related_name="quizzes",
    )
    classroom = models.ForeignKey(
        Classroom,
        on_delete=models.PROTECT,
        related_name="quizzes",
    )
    academic_year = models.ForeignKey(
        Year,
        on_delete=models.PROTECT,
        related_name="quizzes",
    )
    term = models.ForeignKey(
        Term,
        on_delete=models.PROTECT,
        related_name="quizzes",
    )
    duration_minutes = models.PositiveSmallIntegerField(default=30)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    is_published = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20,
        choices=QuizStatusChoices.choices,
        default=QuizStatusChoices.DRAFT,
    )

    class Meta:
        verbose_name = "Kuis"
        verbose_name_plural = "Kuis"

    def __str__(self):
        return self.title


class QuizAttempt(StudentValidationMixin, TimeStampedMixin):
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name="attempts",
    )
    student = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to=STUDENT_LIMIT,
        related_name="quiz_attempts",
    )
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    attempt_number = models.PositiveSmallIntegerField(default=1)

    class Meta:
        verbose_name = "Percobaan Kuis"
        verbose_name_plural = "Percobaan Kuis"
        constraints = [
            models.UniqueConstraint(
                fields=["quiz", "student", "attempt_number"],
                name="unique_quiz_attempt",
            )
        ]

    def __str__(self):
        return f"{self.quiz.title} - {self.student.username} - Attempt {self.attempt_number}"
