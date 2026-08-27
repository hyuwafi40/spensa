from django import forms
from core.forms.base import StyledFormMixin, ActiveYearRequiredMixin
from core.models.academic import ActiveSubject
from core.models.account import CustomUser
from core.utils.constants import JobChoices


class ActiveSubjectForm(StyledFormMixin, ActiveYearRequiredMixin, forms.ModelForm):
    teacher = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(job=JobChoices.TEACHER), label="Guru"
    )

    class Meta:
        model = ActiveSubject
        fields = ["subject", "classroom", "teacher"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["subject"].widget.attrs["class"] = "form-input"
        self.fields["classroom"].widget.attrs["class"] = "form-input"
        self.fields["teacher"].widget.attrs["class"] = "form-input"
        self.fields["teacher"].label_from_instance = (
            lambda obj: obj.get_full_name() or obj.username
        )
