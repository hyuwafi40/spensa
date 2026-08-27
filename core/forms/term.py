from django import forms
from core.forms.base import StyledFormMixin
from core.models.academic import Term


class TermForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Term
        fields = ["name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs["class"] = "form-input"
