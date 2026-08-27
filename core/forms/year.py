from django import forms
from core.forms.base import StyledFormMixin
from core.models.academic import Year
from core.utils.validators import validate_year


class YearForm(StyledFormMixin, forms.ModelForm):
    start_year = forms.CharField(
        max_length=4, validators=[validate_year], required=True
    )
    finish_year = forms.CharField(
        max_length=4, validators=[validate_year], required=True
    )

    class Meta:
        model = Year
        fields = ["start_year", "finish_year"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["start_year"].widget.attrs["placeholder"] = "2026"
        self.fields["finish_year"].widget.attrs["placeholder"] = "2027"

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get("start_year")
        finish = cleaned_data.get("finish_year")
        if start and finish and int(finish) <= int(start):
            raise forms.ValidationError(
                "Tahun selesai harus lebih besar dari tahun mulai."
            )
        return cleaned_data
