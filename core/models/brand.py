from django.db import models
from solo.models import SingletonModel
from core.models.base import TimeStampedMixin, SlugMixin
from core.utils.constants import (
    SCHOOL_TYPE_CHOICES,
    SCHOOL_STATUS_CHOICES,
    ACCREDITATION_CHOICES,
)


class Brand(TimeStampedMixin, SlugMixin):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    version = models.CharField(max_length=50, blank=True)
    tahun = models.CharField(max_length=20, blank=True)
    logo = models.URLField(blank=True)
    instagram = models.URLField(default="https://www.instagram.com/hamdayuwafii/")
    youtube = models.URLField(default="https://www.youtube.com/@hamdayuwafii")
    tiktok = models.URLField(default="https://www.tiktok.com/@hamdayuwafii")
    facebook = models.URLField(default="https://web.facebook.com/hamdayuwafii/")
    developer = models.CharField(max_length=150, default="Hamdan Yuwafi")

    def get_slug_source(self):
        return self.name

    class Meta:
        verbose_name = "Brand"
        verbose_name_plural = "Brand"

    def __str__(self):
        return self.name


class School(SingletonModel, TimeStampedMixin, SlugMixin):
    name = models.CharField(max_length=200, blank=True, default="")
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    logo = models.URLField(blank=True, null=True)
    npsn = models.CharField(max_length=20, blank=True, null=True)
    nss = models.CharField(max_length=20, blank=True, null=True)
    accreditation = models.CharField(max_length=30, choices=ACCREDITATION_CHOICES, blank=True, null=True)
    school_type = models.CharField(max_length=20, choices=SCHOOL_TYPE_CHOICES, blank=True, null=True)
    status = models.CharField(max_length=20, choices=SCHOOL_STATUS_CHOICES, blank=True, null=True)
    headmaster_name = models.CharField(max_length=150, blank=True, null=True)
    headmaster_nip = models.CharField(max_length=30, blank=True, null=True)
    established_year = models.CharField(max_length=10, blank=True, null=True)
    fax = models.CharField(max_length=30, blank=True, null=True)
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    province = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    village = models.CharField(max_length=100, blank=True, null=True)
    curriculum = models.CharField(max_length=100, blank=True, null=True)
    since = models.CharField(max_length=20, blank=True, null=True)

    def get_slug_source(self):
        return self.name or "sekolah"

    class Meta:
        verbose_name = "Sekolah"
        verbose_name_plural = "Sekolah"

    def __str__(self):
        return self.name or "Sekolah"
