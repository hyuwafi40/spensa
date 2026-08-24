from django.contrib import admin
from solo.admin import SingletonModelAdmin
from core.admin.base import BaseModelAdminMixin
from core.models.brand import Brand, School


@admin.register(Brand)
class BrandAdmin(BaseModelAdminMixin, admin.ModelAdmin):
    list_display = ("name", "version", "developer", "updated_at")
    search_fields = ("name", "developer")
    readonly_fields = ("slug",)


@admin.register(School)
class SchoolAdmin(BaseModelAdminMixin, SingletonModelAdmin):
    readonly_fields = ("slug",)
