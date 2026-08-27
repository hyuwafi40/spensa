from django import forms
from core.forms.base import StyledFormMixin
from core.models.academic import ActiveYear


class ActiveYearForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = ActiveYear
        fields = ["year", "term"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["year"].widget.attrs["class"] = "form-input"
        self.fields["term"].widget.attrs["class"] = "form-input"
