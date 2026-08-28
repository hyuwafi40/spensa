from django import forms
from core.forms.base import StyledFormMixin
from core.models.account import CustomUser, Profile
from core.utils.constants import COMMON_PROFILE_FIELDS, ROLE_PROFILE_FIELDS


class UserProfileForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].label = "Nama Depan"
        self.fields["last_name"].label = "Nama Belakang"
        self.fields["email"].label = "Alamat Email"

        placeholders = {
            "first_name": "Contoh: Ahmad",
            "last_name": "Contoh: Fauzan",
            "email": "Contoh: nama@email.com",
        }
        for field_name, placeholder in placeholders.items():
            self.fields[field_name].widget.attrs["placeholder"] = placeholder


class ProfileDetailForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"

    labels = {
        "code": "Nomor Induk (NISN/NIP)",
        "photo": "URL Foto",
        "phone": "Nomor Telepon Aktif",
        "address": "Alamat Lengkap",
        "gender": "Jenis Kelamin",
        "birth_date": "Tanggal Lahir",
        "birth_place": "Tempat Lahir",
        "religion": "Agama",
        "nisn": "NISN",
        "nis": "NIS",
        "class_level": "Kelas",
        "major": "Jurusan",
        "parent_name": "Nama Orang Tua",
        "parent_phone": "Nomor Telepon Orang Tua",
        "nuptk": "NUPTK",
        "subject": "Mata Pelajaran",
        "position": "Posisi",
        "institution": "Institusi",
        "nip": "NIP",
        "employee_id": "ID Pegawai",
        "bio": "Biografi Singkat",
        "website": "Situs Pribadi",
        "github": "GitHub",
        "stack_overflow": "Stack Overflow",
        "department": "Divisi/Bagian",
        "fax": "Nomor Fax",
        "employee_status": "Status Kepegawaian",
        "start_date": "Tanggal Mulai Bekerja",
        "education_background": "Pendidikan Terakhir",
        "years_of_experience": "Pengalaman Mengajar (tahun)",
        "certification": "Sertifikasi Pendidik",
        "academic_degree": "Gelar Akademik",
        "nik": "NIK",
        "blood_type": "Golongan Darah",
        "height": "Tinggi Badan (cm)",
        "weight": "Berat Badan (kg)",
        "hobby": "Hobi",
        "previous_school": "Asal Sekolah",
        "graduation_year": "Tahun Lulus",
        "counselor": "Guru BK/Wali",
        "scholarship_status": "Status Beasiswa",
        "transportation": "Transportasi",
        "father_name": "Nama Ayah",
        "mother_name": "Nama Ibu",
        "father_phone": "Nomor Telepon Ayah",
        "mother_phone": "Nomor Telepon Ibu",
        "parent_address": "Alamat Orang Tua",
        "guardian_name": "Nama Wali",
    }

    placeholders = {
        "code": "Contoh: 1234567890",
        "photo": "https://...",
        "phone": "08xxxxxxxxxx",
        "address": "Jl. Contoh No. 1",
        "gender": "Pilih jenis kelamin",
        "birth_date": "YYYY-MM-DD",
        "birth_place": "Nama kota/kabupaten",
        "religion": "Pilih agama",
        "nisn": "Nomor induk siswa nasional",
        "nis": "Nomor induk sekolah",
        "class_level": "Pilih kelas",
        "major": "Jurusan/Program",
        "parent_name": "Nama orang tua/wali",
        "parent_phone": "08xxxxxxxxxx",
        "nuptk": "Nomor unik pendidik",
        "subject": "Pilih mata pelajaran",
        "position": "Jabatan/posisi",
        "institution": "Nama institusi",
        "nip": "Nomor induk pegawai",
        "employee_id": "ID kepegawaian",
        "bio": "Deskripsi singkat tentang Anda",
        "website": "https://...",
        "github": "https://github.com/username",
        "stack_overflow": "https://stackoverflow.com/users/...",
        "department": "Divisi/bagian",
        "fax": "Nomor fax kantor",
        "employee_status": "Pilih status",
        "start_date": "YYYY-MM-DD",
        "education_background": "S1/S2/S3",
        "years_of_experience": "Lama pengalaman",
        "certification": "Jenis sertifikasi",
        "academic_degree": "S.Pd, M.Pd, dll",
        "nik": "Nomor induk kependudukan",
        "blood_type": "Pilih golongan darah",
        "height": "Tinggi badan",
        "weight": "Berat badan",
        "hobby": "Hobi/kegemaran",
        "previous_school": "Asal sekolah sebelumnya",
        "graduation_year": "Tahun lulus",
        "counselor": "Nama guru BK/wali",
        "scholarship_status": "Pilih status",
        "transportation": "Moda transportasi",
        "father_name": "Nama ayah",
        "mother_name": "Nama ibu",
        "father_phone": "08xxxxxxxxxx",
        "mother_phone": "08xxxxxxxxxx",
        "parent_address": "Alamat orang tua/wali",
        "guardian_name": "Nama wali (jika berbeda)",
    }

    def __init__(self, *args, **kwargs):
        self.role = kwargs.pop("role", None)
        super().__init__(*args, **kwargs)

        if "user" in self.fields:
            del self.fields["user"]

        allowed_fields = COMMON_PROFILE_FIELDS.copy()
        if self.role:
            allowed_fields += ROLE_PROFILE_FIELDS.get(self.role, [])

        for name in list(self.fields):
            if name not in allowed_fields:
                del self.fields[name]
            else:
                self.fields[name].label = self.labels.get(
                    name, name.replace("_", " ").title()
                )
                placeholder = self.placeholders.get(name)
                if placeholder:
                    self.fields[name].widget.attrs["placeholder"] = placeholder

        if self.instance and self.instance.pk:
            self.fields["code"].disabled = True
