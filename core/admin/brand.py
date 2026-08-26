from django.contrib import admin
from solo.admin import SingletonModelAdmin
from core.admin.base import BaseModelAdminMixin
from core.models.brand import Brand, School


@admin.register(Brand)
class BrandAdmin(BaseModelAdminMixin, SingletonModelAdmin):
    readonly_fields = ("slug",)


@admin.register(School)
class SchoolAdmin(BaseModelAdminMixin, SingletonModelAdmin):
    readonly_fields = ("slug",)
