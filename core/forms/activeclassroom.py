from django import forms
from core.forms.base import StyledFormMixin, ActiveYearRequiredMixin
from core.models.academic import ActiveClassroom, ActiveStudent, Classroom
from core.models.account import CustomUser
from core.utils.constants import JobChoices


class ActiveClassroomForm(StyledFormMixin, ActiveYearRequiredMixin, forms.ModelForm):
    teacher = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(job=JobChoices.TEACHER), label="Wali Kelas"
    )

    class Meta:
        model = ActiveClassroom
        fields = ["classroom", "teacher", "quota"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["classroom"].widget.attrs["class"] = "form-input"
        self.fields["teacher"].widget.attrs["class"] = "form-input"
        self.fields["teacher"].label_from_instance = (
            lambda obj: obj.get_full_name() or obj.username
        )
        self.fields["quota"].widget.attrs["class"] = "form-input"

        if self.active_year:
            if self.instance and self.instance.pk:
                classroom_qs = Classroom.objects.exclude(
                    active_classrooms__active_year=self.active_year
                ).exclude(pk=self.instance.classroom.pk)
                teacher_qs = (
                    CustomUser.objects.filter(job=JobChoices.TEACHER)
                    .exclude(active_classrooms__active_year=self.active_year)
                    .exclude(pk=self.instance.teacher.pk)
                )
            else:
                classroom_qs = Classroom.objects.exclude(
                    active_classrooms__active_year=self.active_year
                )
                teacher_qs = CustomUser.objects.filter(job=JobChoices.TEACHER).exclude(
                    active_classrooms__active_year=self.active_year
                )

            self.fields["classroom"].queryset = classroom_qs
            self.fields["teacher"].queryset = teacher_qs


class ActiveStudentForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = ActiveStudent
        fields = ["student"]

    def __init__(self, *args, **kwargs):
        self.classroom = kwargs.pop("classroom", None)
        super().__init__(*args, **kwargs)
        self.fields["student"].widget.attrs["class"] = "form-input"
        self.fields["student"].label_from_instance = (
            lambda obj: f"{obj.get_full_name() or obj.username} ({obj.get_job_display()})"
        )

        if self.classroom:
            active_year = self.classroom.active_year
            if self.instance and self.instance.pk:
                student_qs = (
                    CustomUser.objects.filter(job=JobChoices.STUDENT)
                    .exclude(active_students__active_year=active_year)
                    .exclude(pk=self.instance.student.pk)
                )
            else:
                student_qs = CustomUser.objects.filter(job=JobChoices.STUDENT).exclude(
                    active_students__active_year=active_year
                )

            self.fields["student"].queryset = student_qs

    def clean(self):
        cleaned_data = super().clean()
        if not self.classroom:
            raise forms.ValidationError("Kelas belum dipilih.")
        active_year = self.classroom.active_year
        quota = self.classroom.quota
        current_count = ActiveStudent.objects.filter(classroom=self.classroom).count()
        if current_count >= quota:
            raise forms.ValidationError("Kuota kelas sudah penuh.")
        student = cleaned_data.get("student")
        if student:
            exists = (
                ActiveStudent.objects.filter(
                    student=student,
                    active_year=active_year,
                )
                .exclude(pk=self.instance.pk if self.instance else None)
                .exists()
            )
            if exists:
                raise forms.ValidationError(
                    "Siswa sudah terdaftar di kelas lain pada tahun ajaran ini."
                )
        return cleaned_data

    def save(self, commit=True):
        obj = super().save(commit=False)
        obj.classroom = self.classroom
        obj.active_year = self.classroom.active_year
        if commit:
            obj.save()
        return obj
