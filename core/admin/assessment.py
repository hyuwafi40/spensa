from django.contrib import admin
from core.admin.base import BaseModelAdminMixin
from core.models.account import CustomUser
from core.models.assessment import Assessment
from core.utils.constants import JobChoices


@admin.register(Assessment)
class AssessmentAdmin(BaseModelAdminMixin, admin.ModelAdmin):
    list_display = (
        "student",
        "subject",
        "active_year",
        "daily_score",
        "midterm_score",
        "final_score",
        "total_score",
        "grade_letter",
        "updated_at",
    )
    list_filter = ("active_year", "subject")
    search_fields = ("student__username", "subject__name")
    list_select_related = (
        "student",
        "subject",
        "active_year__year",
        "active_year__term",
        "teacher",
    )
    readonly_fields = ("daily_score", "total_score", "grade_letter")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "student":
            kwargs["queryset"] = CustomUser.objects.filter(job=JobChoices.STUDENT)
        elif db_field.name == "teacher":
            kwargs["queryset"] = CustomUser.objects.filter(job=JobChoices.TEACHER)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
