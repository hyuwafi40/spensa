from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from core.models.account import CustomUser
from core.models.academic import Classroom, Subject, Term, Year
from core.models.base import TimeStampedMixin
from core.utils.calculations import calculate_grade
from core.utils.constants import (
    AssignmentStatusChoices,
    AssignmentTypeChoices,
    DifficultyChoices,
    ExamStatusChoices,
    JobChoices,
    QuestionTypeChoices,
    QuizStatusChoices,
    SubmissionStatusChoices,
)
from core.utils.services import validate_student, validate_teacher


class Material(TimeStampedMixin):
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
        limit_choices_to={"job": JobChoices.TEACHER},
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

    def clean(self):
        validate_teacher(self.teacher)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Materi Ajar"
        verbose_name_plural = "Materi Ajar"

    def __str__(self):
        return self.title


class Assignment(TimeStampedMixin):
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
        limit_choices_to={"job": JobChoices.TEACHER},
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

    def clean(self):
        validate_teacher(self.teacher)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Tugas"
        verbose_name_plural = "Tugas"

    def __str__(self):
        return self.title


class AssignmentSubmission(TimeStampedMixin):
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name="submissions",
    )
    student = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={"job": JobChoices.STUDENT},
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

    def clean(self):
        validate_student(self.student)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

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


class QuestionBank(TimeStampedMixin):
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
        limit_choices_to={"job": JobChoices.TEACHER},
        related_name="question_banks",
    )
    is_public = models.BooleanField(default=False)

    def clean(self):
        validate_teacher(self.teacher)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Bank Soal"
        verbose_name_plural = "Bank Soal"

    def __str__(self):
        return self.name


class Question(TimeStampedMixin):
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
        limit_choices_to={"job": JobChoices.TEACHER},
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

    def clean(self):
        validate_teacher(self.teacher)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

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


class Quiz(TimeStampedMixin):
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
        limit_choices_to={"job": JobChoices.TEACHER},
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
    duration_minutes = models.PositiveSmallIntegerField(default=30)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    is_published = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20,
        choices=QuizStatusChoices.choices,
        default=QuizStatusChoices.DRAFT,
    )

    def clean(self):
        validate_teacher(self.teacher)
        if self.start_time and self.end_time and self.start_time >= self.end_time:
            raise ValidationError("Waktu mulai harus sebelum waktu selesai.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Kuis"
        verbose_name_plural = "Kuis"

    def __str__(self):
        return self.title


class QuizAttempt(TimeStampedMixin):
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name="attempts",
    )
    student = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={"job": JobChoices.STUDENT},
        related_name="quiz_attempts",
    )
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    attempt_number = models.PositiveSmallIntegerField(default=1)

    def clean(self):
        validate_student(self.student)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

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


class Exam(TimeStampedMixin):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    subject = models.ForeignKey(
        Subject,
        on_delete=models.PROTECT,
        related_name="exams",
    )
    teacher = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        limit_choices_to={"job": JobChoices.TEACHER},
        related_name="exams",
    )
    classroom = models.ForeignKey(
        Classroom,
        on_delete=models.PROTECT,
        related_name="exams",
    )
    academic_year = models.ForeignKey(
        Year,
        on_delete=models.PROTECT,
        related_name="exams",
    )
    duration_minutes = models.PositiveSmallIntegerField(default=90)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    randomize_questions = models.BooleanField(default=False)
    proctoring_enabled = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20,
        choices=ExamStatusChoices.choices,
        default=ExamStatusChoices.DRAFT,
    )

    def clean(self):
        validate_teacher(self.teacher)
        if self.start_time >= self.end_time:
            raise ValidationError("Waktu mulai harus sebelum waktu selesai.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Ujian"
        verbose_name_plural = "Ujian"

    def __str__(self):
        return self.title


class ExamAttempt(TimeStampedMixin):
    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        related_name="attempts",
    )
    student = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={"job": JobChoices.STUDENT},
        related_name="exam_attempts",
    )
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    is_completed = models.BooleanField(default=False)

    def clean(self):
        validate_student(self.student)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Percobaan Ujian"
        verbose_name_plural = "Percobaan Ujian"
        constraints = [
            models.UniqueConstraint(
                fields=["exam", "student"],
                name="unique_exam_attempt",
            )
        ]

    def __str__(self):
        return f"{self.exam.title} - {self.student.username}"


class Grade(TimeStampedMixin):
    student = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={"job": JobChoices.STUDENT},
        related_name="grades",
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.PROTECT,
        related_name="grades",
    )
    term = models.ForeignKey(
        Term,
        on_delete=models.PROTECT,
        related_name="grades",
    )
    teacher = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        limit_choices_to={"job": JobChoices.TEACHER},
        related_name="graded_subjects",
    )
    daily_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
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
        self.total_score, self.grade_letter = calculate_grade(
            self.daily_score, self.midterm_score, self.final_score
        )
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Nilai"
        verbose_name_plural = "Nilai"
        constraints = [
            models.UniqueConstraint(
                fields=["student", "subject", "term"],
                name="unique_grade",
            )
        ]

    def __str__(self):
        return f"{self.student.username} - {self.subject.name} - {self.term.name}"


class ReportCard(TimeStampedMixin):
    student = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={"job": JobChoices.STUDENT},
        related_name="report_cards",
    )
    term = models.ForeignKey(
        Term,
        on_delete=models.PROTECT,
        related_name="report_cards",
    )
    file = models.FileField(upload_to="report_cards/%Y/%m/%d/")
    generated_at = models.DateTimeField(auto_now_add=True)
    generated_by = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        limit_choices_to={
            "job__in": [
                JobChoices.TEACHER,
                JobChoices.ADMINISTRATOR,
                JobChoices.DEVELOPER,
            ]
        },
        related_name="generated_report_cards",
    )

    class Meta:
        verbose_name = "Rapor"
        verbose_name_plural = "Rapor"
        constraints = [
            models.UniqueConstraint(
                fields=["student", "term"],
                name="unique_report_card",
            )
        ]

    def __str__(self):
        return f"{self.student.username} - {self.term.name}"
