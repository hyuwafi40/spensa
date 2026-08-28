from django.contrib.auth.models import AbstractUser
from django.db import models
from core.models.base import TimeStampedMixin
from core.utils.constants import (
    BloodTypeChoices,
    ClassLevelChoices,
    EmployeeStatusChoices,
    GenderChoices,
    JobChoices,
    ReligionChoices,
    ScholarshipStatusChoices,
    SubjectChoices,
)
from core.utils.managers import CustomUserManager
from core.utils.services import set_role_flags
from core.utils.validators import validate_numeric


class CustomUser(AbstractUser):
    job = models.CharField(
        max_length=20, choices=JobChoices.choices, default=JobChoices.STUDENT
    )

    objects = CustomUserManager()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_job = self.job

    def save(self, *args, **kwargs):
        if self.pk is None or self.job != self._original_job:
            set_role_flags(self, self.job)
            self._original_job = self.job
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Pengguna"
        verbose_name_plural = "Pengguna"


class Profile(TimeStampedMixin):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="profile"
    )
    code = models.CharField(max_length=50, unique=True, validators=[validate_numeric])
    photo = models.URLField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    gender = models.CharField(
        max_length=10, choices=GenderChoices.choices, blank=True, null=True
    )
    birth_date = models.DateField(blank=True, null=True)
    birth_place = models.CharField(max_length=100, blank=True, null=True)
    religion = models.CharField(
        max_length=20, choices=ReligionChoices.choices, blank=True, null=True
    )
    nisn = models.CharField(max_length=50, blank=True, null=True)
    nis = models.CharField(max_length=50, blank=True, null=True)
    class_level = models.CharField(
        max_length=20, choices=ClassLevelChoices.choices, blank=True, null=True
    )
    major = models.CharField(max_length=100, blank=True, null=True)
    parent_name = models.CharField(max_length=150, blank=True, null=True)
    parent_phone = models.CharField(max_length=20, blank=True, null=True)
    nuptk = models.CharField(max_length=50, blank=True, null=True)
    subject = models.CharField(
        max_length=50, choices=SubjectChoices.choices, blank=True, null=True
    )
    position = models.CharField(max_length=100, blank=True, null=True)
    institution = models.CharField(max_length=150, blank=True, null=True)
    nip = models.CharField(max_length=50, blank=True, null=True)
    employee_id = models.CharField(max_length=50, blank=True, null=True)

    bio = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    stack_overflow = models.URLField(blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    fax = models.CharField(max_length=30, blank=True, null=True)
    employee_status = models.CharField(
        max_length=50, choices=EmployeeStatusChoices.choices, blank=True, null=True
    )
    start_date = models.DateField(blank=True, null=True)
    education_background = models.TextField(blank=True, null=True)
    years_of_experience = models.PositiveSmallIntegerField(blank=True, null=True)
    certification = models.CharField(max_length=100, blank=True, null=True)
    academic_degree = models.CharField(max_length=50, blank=True, null=True)
    nik = models.CharField(max_length=20, blank=True, null=True)
    blood_type = models.CharField(
        max_length=10, choices=BloodTypeChoices.choices, blank=True, null=True
    )
    height = models.PositiveSmallIntegerField(blank=True, null=True)
    weight = models.PositiveSmallIntegerField(blank=True, null=True)
    hobby = models.CharField(max_length=100, blank=True, null=True)
    previous_school = models.CharField(max_length=150, blank=True, null=True)
    graduation_year = models.CharField(max_length=4, blank=True, null=True)
    counselor = models.CharField(max_length=150, blank=True, null=True)
    scholarship_status = models.CharField(
        max_length=50, choices=ScholarshipStatusChoices.choices, blank=True, null=True
    )
    transportation = models.CharField(max_length=100, blank=True, null=True)
    father_name = models.CharField(max_length=150, blank=True, null=True)
    mother_name = models.CharField(max_length=150, blank=True, null=True)
    father_phone = models.CharField(max_length=20, blank=True, null=True)
    mother_phone = models.CharField(max_length=20, blank=True, null=True)
    parent_address = models.TextField(blank=True, null=True)
    guardian_name = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.code}"

    class Meta:
        verbose_name = "Profil"
        verbose_name_plural = "Profil"
