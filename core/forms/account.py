from django import forms
from core.forms.base import StyledFormMixin
from core.models.account import CustomUser, Profile
from core.utils.constants import JobChoices


class CustomUserForm(StyledFormMixin, forms.ModelForm):
    code = forms.CharField(max_length=50, required=True)
    job = forms.ChoiceField(
        choices=[c for c in JobChoices.choices if c[0] != JobChoices.DEVELOPER]
    )

    class Meta:
        model = CustomUser
        fields = [
            "first_name",
            "last_name",
            "email",
            "job",
        ]

    def __init__(self, *args, **kwargs):
        instance = kwargs.get("instance")
        if instance and hasattr(instance, "profile"):
            initial = kwargs.get("initial", {})
            initial["code"] = instance.profile.code
            kwargs["initial"] = initial
        super().__init__(*args, **kwargs)
        placeholders = {
            "code": "Masukkan NIP/NISN",
            "first_name": "Masukkan nama depan",
            "last_name": "Masukkan nama belakang",
            "email": "Masukkan alamat email",
            "job": "Pilih peran pengguna",
        }
        for field_name, placeholder in placeholders.items():
            if field_name in self.fields:
                self.fields[field_name].widget.attrs["placeholder"] = placeholder

    def clean_code(self):
        code = self.cleaned_data.get("code").strip()
        if (
            CustomUser.objects.exclude(pk=self.instance.pk)
            .filter(username=code)
            .exists()
        ):
            raise forms.ValidationError("Kode sudah digunakan oleh akun lain.")
        return code

    def save(self, commit=True):
        user = super().save(commit=False)
        code = self.cleaned_data["code"]
        user.username = code
        if self.instance.pk is None:
            user.set_password("baskara123")
        if commit:
            user.save()
            profile, created = Profile.objects.get_or_create(user=user)
            profile.code = code
            profile.save()
        return user
