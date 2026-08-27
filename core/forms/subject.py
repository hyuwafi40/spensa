from django import forms
from core.forms.base import StyledFormMixin
from core.models.academic import Subject


class SubjectForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Subject
        fields = ["code", "name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["code"].widget.attrs["placeholder"] = "Kode (3-6 huruf)"
        self.fields["name"].widget.attrs["placeholder"] = "Nama mata pelajaran"
