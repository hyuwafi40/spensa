from django.contrib import admin
from core.admin.base import BaseModelAdminMixin
from core.models.journal import TeacherJournal, StudentJournal
from core.models.account import CustomUser
from core.utils.constants import JobChoices


@admin.register(TeacherJournal)
class TeacherJournalAdmin(BaseModelAdminMixin, admin.ModelAdmin):
    list_display = (
        "teacher",
        "get_activity_display",
        "get_module_display",
        "target_name",
        "created_at",
    )
    list_filter = ("activity", "module", "created_at")
    search_fields = ("teacher__username", "teacher__first_name", "target_name", "notes")
    list_select_related = ("teacher",)
    readonly_fields = ("created_at", "updated_at")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "teacher":
            kwargs["queryset"] = CustomUser.objects.filter(job=JobChoices.TEACHER)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(StudentJournal)
class StudentJournalAdmin(BaseModelAdminMixin, admin.ModelAdmin):
    list_display = (
        "student",
        "get_activity_display",
        "get_module_display",
        "target_name",
        "created_at",
    )
    list_filter = ("activity", "module", "created_at")
    search_fields = ("student__username", "student__first_name", "target_name", "notes")
    list_select_related = ("student",)
    readonly_fields = ("created_at", "updated_at")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "student":
            kwargs["queryset"] = CustomUser.objects.filter(job=JobChoices.STUDENT)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
