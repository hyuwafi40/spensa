from django.contrib import admin
from core.admin.base import BaseModelAdminMixin
from core.models.account import CustomUser
from core.models.log import DeveloperLog


@admin.register(DeveloperLog)
class DeveloperLogAdmin(BaseModelAdminMixin, admin.ModelAdmin):
    list_display = (
        "level",
        "event",
        "module",
        "action",
        "object_repr",
        "user",
        "ip_address",
        "created_at",
    )
    list_filter = ("level", "method", "status_code", "module", "action", "created_at")
    search_fields = ("event", "path", "user__username", "ip_address", "object_repr")
    list_select_related = ("user",)
    readonly_fields = [field.name for field in DeveloperLog._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_module_permission(self, request):
        return request.user.is_superuser

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = CustomUser.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
