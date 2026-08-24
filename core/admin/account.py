from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from core.admin.base import BaseModelAdminMixin
from core.models.account import CustomUser, Profile
from core.utils.services import generate_username


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(required=False)

    class Meta(UserCreationForm.Meta):
        model = CustomUser


class ProfileInline(admin.StackedInline):
    model = Profile
    extra = 0
    min_num = 1
    max_num = 1
    can_delete = False
    fields = [
        field.name
        for field in Profile._meta.fields
        if field.name not in ("user", "id", "created_at", "updated_at")
    ]


@admin.register(CustomUser)
class CustomUserAdmin(BaseModelAdminMixin, UserAdmin):
    add_form = CustomUserCreationForm
    inlines = [ProfileInline]
    fieldsets = UserAdmin.fieldsets + (("Job", {"fields": ("job",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (("Job", {"fields": ("job",)}),)

    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == "username":
            field.required = False
        return field

    def save_model(self, request, obj, form, change):
        code = None
        for key in request.POST:
            if key.endswith("-code"):
                code = request.POST.get(key)
                break
        if code:
            obj.username = code
        elif not obj.username:
            obj.username = generate_username()
        super().save_model(request, obj, form, change)
