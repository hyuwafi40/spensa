from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView
from core.forms.profile import UserProfileForm, ProfileDetailForm
from core.models.account import Profile
from core.utils.constants import COMMON_PROFILE_FIELDS, ROLE_PROFILE_FIELDS


class ProfilePageView(LoginRequiredMixin, TemplateView):
    template_name = "core/profile.html"

    def _get_profile_fields(self, user, profile):
        fields = []
        fields.append({"label": "Username", "value": user.username, "icon": "fa-user"})
        fields.append(
            {
                "label": "Nama Lengkap",
                "value": user.get_full_name() or "-",
                "icon": "fa-id-badge",
            }
        )
        fields.append(
            {"label": "Email", "value": user.email or "-", "icon": "fa-envelope"}
        )
        fields.append(
            {"label": "Role", "value": user.get_job_display(), "icon": "fa-user-tag"}
        )

        if not profile:
            return fields

        common_field_map = {
            "code": ("Nomor Induk (NISN/NIP)", "fa-hashtag"),
            "phone": ("Nomor Telepon", "fa-phone"),
            "address": ("Alamat Lengkap", "fa-location-dot"),
            "gender": ("Jenis Kelamin", "fa-venus-mars"),
            "birth_date": ("Tanggal Lahir", "fa-cake-candles"),
            "birth_place": ("Tempat Lahir", "fa-location-pin"),
            "religion": ("Agama", "fa-book"),
        }
        role_field_map = {
            "nisn": ("NISN", "fa-hashtag"),
            "nis": ("NIS", "fa-hashtag"),
            "class_level": ("Kelas", "fa-graduation-cap"),
            "major": ("Jurusan", "fa-layer-group"),
            "parent_name": ("Nama Orang Tua", "fa-user-tie"),
            "parent_phone": ("Telepon Orang Tua", "fa-phone"),
            "nuptk": ("NUPTK", "fa-id-card"),
            "subject": ("Mata Pelajaran", "fa-chalkboard-user"),
            "position": ("Posisi", "fa-briefcase"),
            "institution": ("Institusi", "fa-building"),
            "nip": ("NIP", "fa-id-badge"),
            "employee_id": ("ID Pegawai", "fa-id-card"),
            "bio": ("Biografi Singkat", "fa-align-left"),
            "website": ("Situs Pribadi", "fa-globe"),
            "github": ("GitHub", "fa-brands fa-github"),
            "stack_overflow": ("Stack Overflow", "fa-brands fa-stack-overflow"),
            "department": ("Divisi/Bagian", "fa-building"),
            "fax": ("Nomor Fax", "fa-fax"),
            "employee_status": ("Status Kepegawaian", "fa-id-card"),
            "start_date": ("Tanggal Mulai Bekerja", "fa-calendar"),
            "education_background": ("Pendidikan Terakhir", "fa-graduation-cap"),
            "years_of_experience": ("Pengalaman Mengajar", "fa-clock"),
            "certification": ("Sertifikasi Pendidik", "fa-certificate"),
            "academic_degree": ("Gelar Akademik", "fa-user-graduate"),
            "nik": ("NIK", "fa-id-card"),
            "blood_type": ("Golongan Darah", "fa-droplet"),
            "height": ("Tinggi Badan", "fa-ruler"),
            "weight": ("Berat Badan", "fa-weight-scale"),
            "hobby": ("Hobi", "fa-heart"),
            "previous_school": ("Asal Sekolah", "fa-school"),
            "graduation_year": ("Tahun Lulus", "fa-calendar"),
            "counselor": ("Guru BK/Wali", "fa-user-tie"),
            "scholarship_status": ("Status Beasiswa", "fa-award"),
            "transportation": ("Transportasi", "fa-bus"),
            "father_name": ("Nama Ayah", "fa-user"),
            "mother_name": ("Nama Ibu", "fa-user"),
            "father_phone": ("Telepon Ayah", "fa-phone"),
            "mother_phone": ("Telepon Ibu", "fa-phone"),
            "parent_address": ("Alamat Orang Tua", "fa-location-dot"),
            "guardian_name": ("Nama Wali", "fa-user-tie"),
        }

        allowed_fields = COMMON_PROFILE_FIELDS.copy()
        if user.job:
            allowed_fields += ROLE_PROFILE_FIELDS.get(user.job, [])

        choice_fields = {
            "gender": "get_gender_display",
            "religion": "get_religion_display",
            "class_level": "get_class_level_display",
            "subject": "get_subject_display",
            "employee_status": "get_employee_status_display",
            "blood_type": "get_blood_type_display",
            "scholarship_status": "get_scholarship_status_display",
        }
        date_fields = {"birth_date", "start_date"}
        unit_fields = {"height": "cm", "weight": "kg", "years_of_experience": "tahun"}

        for field_name in allowed_fields:
            if field_name == "photo":
                continue
            label, icon = (
                common_field_map.get(field_name)
                or role_field_map.get(field_name)
                or (field_name.replace("_", " ").title(), "fa-circle-info")
            )
            raw_value = getattr(profile, field_name, None)

            if field_name in choice_fields:
                method_name = choice_fields[field_name]
                value = getattr(profile, method_name)() if raw_value else "-"
            elif field_name in date_fields:
                value = raw_value.strftime("%d %b %Y") if raw_value else "-"
            elif field_name in unit_fields:
                if raw_value is not None:
                    value = f"{raw_value} {unit_fields[field_name]}"
                else:
                    value = "-"
            else:
                value = raw_value if raw_value else "-"

            fields.append({"label": label, "value": value, "icon": icon})

        return fields

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        profile = Profile.objects.filter(user=user).first()
        context["user"] = user
        context["profile"] = profile
        context["has_profile"] = profile is not None
        context["profile_fields"] = self._get_profile_fields(user, profile)
        context["breadcrumb_items"] = [
            {"label": "Home", "url": reverse_lazy("core:index")},
            {"label": "Profil", "url": None},
        ]
        return context


class ProfileUpdateView(LoginRequiredMixin, View):
    template_name = "core/profile/form.html"
    success_url = reverse_lazy("core:profile")

    def get(self, request, *args, **kwargs):
        user = request.user
        profile = Profile.objects.filter(user=user).first()
        user_form = UserProfileForm(instance=user)
        profile_form = ProfileDetailForm(instance=profile, role=user.job)
        context = {
            "user_form": user_form,
            "profile_form": profile_form,
            "breadcrumb_items": [
                {"label": "Home", "url": reverse_lazy("core:index")},
                {"label": "Profil", "url": self.success_url},
                {"label": "Edit", "url": None},
            ],
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user = request.user
        profile = Profile.objects.filter(user=user).first()
        user_form = UserProfileForm(request.POST, instance=user)
        profile_form = ProfileDetailForm(request.POST, instance=profile, role=user.job)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_obj = profile_form.save(commit=False)
            profile_obj.user = user
            profile_obj.save()
            messages.success(request, "Profil berhasil diperbarui.")
            return redirect(self.success_url)

        context = {
            "user_form": user_form,
            "profile_form": profile_form,
            "breadcrumb_items": [
                {"label": "Home", "url": reverse_lazy("core:index")},
                {"label": "Profil", "url": self.success_url},
                {"label": "Edit", "url": None},
            ],
        }
        return render(request, self.template_name, context)
