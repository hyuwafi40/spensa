from django import forms
from core.forms.base import StyledFormMixin
from core.models.academic import Classroom


class ClassroomForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Classroom
        fields = ["grade", "name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["grade"].widget.attrs["class"] = "form-input"
        self.fields["name"].widget.attrs["placeholder"] = "Nama kelas (contoh: A, B, 1)"
