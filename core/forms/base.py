from django import forms
from core.models.academic import ActiveYear


class StyledFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(
                field.widget,
                (
                    forms.TextInput,
                    forms.EmailInput,
                    forms.Select,
                    forms.Textarea,
                    forms.URLInput,
                ),
            ):
                field.widget.attrs.setdefault("class", "form-input")
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.setdefault("class", "form-check")


class ActiveYearRequiredMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.active_year = ActiveYear.objects.filter(is_active=True).first()

    def clean(self):
        cleaned_data = super().clean()
        if not self.active_year:
            raise forms.ValidationError(
                "Tidak ada tahun ajaran aktif. Silakan aktifkan satu tahun ajaran terlebih dahulu."
            )
        return cleaned_data

    def save(self, commit=True):
        obj = super().save(commit=False)
        obj.active_year = self.active_year
        if commit:
            obj.save()
        return obj
