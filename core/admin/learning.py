from django.contrib import admin
from core.admin.base import BaseModelAdminMixin
from core.models.account import CustomUser
from core.models.learning import (
    Material,
    Assignment,
    AssignmentSubmission,
    QuestionBank,
    Question,
    AnswerOption,
    Quiz,
    QuizAttempt,
)
from core.utils.constants import JobChoices


@admin.register(Material)
class MaterialAdmin(BaseModelAdminMixin, admin.ModelAdmin):
    list_display = (
        "title",
        "material_type",
        "subject",
        "teacher",
        "classroom",
        "academic_year",
        "updated_at",
    )
    list_filter = ("material_type", "subject", "academic_year")
    search_fields = ("title", "description", "teacher__username")
    list_select_related = ("subject", "teacher", "classroom", "academic_year")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "teacher":
            kwargs["queryset"] = CustomUser.objects.filter(job=JobChoices.TEACHER)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Assignment)
class AssignmentAdmin(BaseModelAdminMixin, admin.ModelAdmin):
    list_display = (
        "title",
        "type",
        "subject",
        "teacher",
        "classroom",
        "term",
        "due_date",
        "status",
        "updated_at",
    )
    list_filter = ("type", "status", "subject", "academic_year", "term")
    search_fields = ("title", "teacher__username", "classroom__name")
    list_select_related = ("subject", "teacher", "classroom", "academic_year", "term")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "teacher":
            kwargs["queryset"] = CustomUser.objects.filter(job=JobChoices.TEACHER)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(AssignmentSubmission)
class AssignmentSubmissionAdmin(BaseModelAdminMixin, admin.ModelAdmin):
    list_display = (
        "assignment",
        "student",
        "submitted_at",
        "score",
        "status",
        "updated_at",
    )
    list_filter = ("status", "assignment")
    search_fields = ("student__username", "assignment__title")
    list_select_related = (
        "assignment",
        "student",
        "assignment__subject",
        "assignment__teacher",
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "student":
            kwargs["queryset"] = CustomUser.objects.filter(job=JobChoices.STUDENT)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(QuestionBank)
class QuestionBankAdmin(BaseModelAdminMixin, admin.ModelAdmin):
    list_display = ("name", "subject", "teacher", "is_public", "updated_at")
    list_filter = ("is_public", "subject")
    search_fields = ("name", "teacher__username")
    list_select_related = ("subject", "teacher")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "teacher":
            kwargs["queryset"] = CustomUser.objects.filter(job=JobChoices.TEACHER)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class AnswerOptionInline(admin.TabularInline):
    model = AnswerOption
    extra = 1
    min_num = 2
    max_num = 6


@admin.register(Question)
class QuestionAdmin(BaseModelAdminMixin, admin.ModelAdmin):
    list_display = (
        "question_text",
        "question_type",
        "difficulty",
        "subject",
        "teacher",
        "points",
        "updated_at",
    )
    list_filter = ("question_type", "difficulty", "subject")
    search_fields = ("question_text", "teacher__username")
    list_select_related = ("question_bank", "subject", "teacher")
    inlines = [AnswerOptionInline]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "teacher":
            kwargs["queryset"] = CustomUser.objects.filter(job=JobChoices.TEACHER)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(AnswerOption)
class AnswerOptionAdmin(BaseModelAdminMixin, admin.ModelAdmin):
    list_display = ("question", "text", "is_correct", "order", "updated_at")
    list_filter = ("is_correct",)
    search_fields = ("text", "question__question_text")
    list_select_related = ("question",)


@admin.register(Quiz)
class QuizAdmin(BaseModelAdminMixin, admin.ModelAdmin):
    list_display = (
        "title",
        "subject",
        "teacher",
        "classroom",
        "term",
        "start_time",
        "end_time",
        "status",
        "updated_at",
    )
    list_filter = ("status", "subject", "academic_year", "term")
    search_fields = ("title", "teacher__username", "classroom__name")
    list_select_related = ("subject", "teacher", "classroom", "academic_year", "term")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "teacher":
            kwargs["queryset"] = CustomUser.objects.filter(job=JobChoices.TEACHER)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(QuizAttempt)
class QuizAttemptAdmin(BaseModelAdminMixin, admin.ModelAdmin):
    list_display = (
        "quiz",
        "student",
        "attempt_number",
        "score",
        "is_completed",
        "start_time",
        "updated_at",
    )
    list_filter = ("is_completed", "quiz")
    search_fields = ("student__username", "quiz__title")
    list_select_related = ("quiz", "student")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "student":
            kwargs["queryset"] = CustomUser.objects.filter(job=JobChoices.STUDENT)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
