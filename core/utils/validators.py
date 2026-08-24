import re
from django.core.exceptions import ValidationError


def validate_numeric(value):
    if not value.isdigit():
        raise ValidationError("Kode harus berupa angka.")
    if len(value.strip()) < 4:
        raise ValidationError("Kode minimal 4 digit.")


def validate_year(value):
    if not re.fullmatch(r"\d{4}", value):
        raise ValidationError("Tahun harus 4 digit angka.")
