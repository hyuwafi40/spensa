from django import forms
from core.models.account import CustomUser, Profile
from core.utils.constants import COMMON_PROFILE_FIELDS, ROLE_PROFILE_FIELDS
from core.utils.collections import (
    PROFILE_FIELD_CONFIG,
    USER_PROFILE_FIELD_CONFIG,
    PROFILE_FIELD_LAYOUT,
)


class UserProfileForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "pf-input",
                "placeholder": "Isi jika ingin mengganti password",
            }
        ),
        required=False,
        label="Password Baru",
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "pf-input", "placeholder": "Ulangi password baru"}
        ),
        required=False,
        label="Konfirmasi Password Baru",
    )

    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, config in USER_PROFILE_FIELD_CONFIG.items():
            if field_name in self.fields:
                self.fields[field_name].label = config.label
                self.fields[field_name].widget.attrs["placeholder"] = config.placeholder
                self.fields[field_name].widget.attrs["class"] = "pf-input"
                self.fields[field_name].widget.attrs["layout"] = "pf-field--half"
        self.fields["password"].widget.attrs["layout"] = "pf-field--full"
        self.fields["password_confirm"].widget.attrs["layout"] = "pf-field--full"

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password or password_confirm:
            if password != password_confirm:
                raise forms.ValidationError(
                    "Password dan konfirmasi password tidak sama."
                )
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user


class ProfileDetailForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        self.role = kwargs.pop("role", None)
        super().__init__(*args, **kwargs)

        if "user" in self.fields:
            del self.fields["user"]

        allowed_fields = COMMON_PROFILE_FIELDS.copy()
        if self.role:
            allowed_fields += ROLE_PROFILE_FIELDS.get(self.role, [])

        for name in list(self.fields):
            if name not in allowed_fields:
                del self.fields[name]
            else:
                config = PROFILE_FIELD_CONFIG.get(name)
                if config:
                    self.fields[name].label = config.label
                    if config.placeholder:
                        self.fields[name].widget.attrs[
                            "placeholder"
                        ] = config.placeholder
                self.fields[name].widget.attrs["class"] = "pf-input"
                layout_class = PROFILE_FIELD_LAYOUT.get(name, "pf-field--half")
                self.fields[name].widget.attrs["layout"] = layout_class

        if self.instance and self.instance.pk:
            self.fields["code"].disabled = True
