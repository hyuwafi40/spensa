from django.contrib import admin
from core.admin.base import BaseModelAdminMixin
from core.models.academic import (
    Year,
    Term,
    Subject,
    Classroom,
    ActiveYear,
    ActiveSubject,
    ActiveClassroom,
    ActiveStudent,
)
from core.models.account import CustomUser


@admin.register(Year)
class YearAdmin(BaseModelAdminMixin, admin.ModelAdmin):
    list_display = ("start_year", "finish_year", "updated_at")
    search_fields = ("start_year", "finish_year")


@admin.register(Term)
class TermAdmin(BaseModelAdminMixin, admin.ModelAdmin):
    list_display = ("name", "updated_at")


@admin.register(Subject)
class SubjectAdmin(BaseModelAdminMixin, admin.ModelAdmin):
    list_display = ("code", "name", "updated_at")
    search_fields = ("code", "name")


@admin.register(Classroom)
class ClassroomAdmin(BaseModelAdminMixin, admin.ModelAdmin):
    list_display = ("grade", "name", "updated_at")
    search_fields = ("name",)
    list_filter = ("grade",)


@admin.register(ActiveYear)
class ActiveYearAdmin(BaseModelAdminMixin, admin.ModelAdmin):
    list_display = ("year", "term", "is_active", "updated_at")
    list_filter = ("is_active", "year", "term")
    list_select_related = ("year", "term")


@admin.register(ActiveSubject)
class ActiveSubjectAdmin(BaseModelAdminMixin, admin.ModelAdmin):
    list_display = ("active_year", "subject", "classroom", "teacher", "updated_at")
    list_filter = ("active_year", "subject", "classroom")
    search_fields = ("subject__name", "teacher__username", "classroom__name")
    list_select_related = (
        "active_year__year",
        "active_year__term",
        "subject",
        "classroom",
        "teacher",
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "teacher":
            kwargs["queryset"] = CustomUser.objects.filter(job="teacher")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(ActiveClassroom)
class ActiveClassroomAdmin(BaseModelAdminMixin, admin.ModelAdmin):
    list_display = ("active_year", "classroom", "teacher", "quota", "updated_at")
    list_filter = ("active_year", "classroom")
    search_fields = ("classroom__name", "teacher__username")
    list_select_related = (
        "active_year__year",
        "active_year__term",
        "classroom",
        "teacher",
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "teacher":
            kwargs["queryset"] = CustomUser.objects.filter(job="teacher")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(ActiveStudent)
class ActiveStudentAdmin(BaseModelAdminMixin, admin.ModelAdmin):
    list_display = ("classroom", "student", "active_year", "updated_at")
    list_filter = ("active_year", "classroom")
    search_fields = ("student__username", "student__first_name", "student__last_name")
    list_select_related = ("classroom__classroom", "student", "active_year")
    readonly_fields = ("active_year",)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "student":
            kwargs["queryset"] = CustomUser.objects.filter(job="student")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
