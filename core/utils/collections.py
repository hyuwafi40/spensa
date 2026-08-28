from collections import namedtuple

ProfileFieldConfig = namedtuple(
    "ProfileFieldConfig",
    ["label", "placeholder", "icon", "type", "unit", "display_method"],
)

USER_PROFILE_FIELD_CONFIG = {
    "first_name": ProfileFieldConfig(
        "Nama Depan", "Contoh: Ahmad", "fa-user", "text", None, None
    ),
    "last_name": ProfileFieldConfig(
        "Nama Belakang", "Contoh: Fauzan", "fa-user", "text", None, None
    ),
    "email": ProfileFieldConfig(
        "Alamat Email", "Contoh: nama@email.com", "fa-envelope", "text", None, None
    ),
}

PROFILE_FIELD_CONFIG = {
    "code": ProfileFieldConfig(
        "Nomor Induk (NISN/NIP)", "Contoh: 1234567890", "fa-hashtag", "text", None, None
    ),
    "photo": ProfileFieldConfig(
        "URL Foto", "https://...", "fa-image", "text", None, None
    ),
    "phone": ProfileFieldConfig(
        "Nomor Telepon Aktif", "08xxxxxxxxxx", "fa-phone", "text", None, None
    ),
    "address": ProfileFieldConfig(
        "Alamat Lengkap", "Jl. Contoh No. 1", "fa-location-dot", "text", None, None
    ),
    "gender": ProfileFieldConfig(
        "Jenis Kelamin",
        "Pilih jenis kelamin",
        "fa-venus-mars",
        "choice",
        None,
        "get_gender_display",
    ),
    "birth_date": ProfileFieldConfig(
        "Tanggal Lahir", "YYYY-MM-DD", "fa-cake-candles", "date", None, None
    ),
    "birth_place": ProfileFieldConfig(
        "Tempat Lahir", "Nama kota/kabupaten", "fa-location-pin", "text", None, None
    ),
    "religion": ProfileFieldConfig(
        "Agama", "Pilih agama", "fa-book", "choice", None, "get_religion_display"
    ),
    "nisn": ProfileFieldConfig(
        "NISN", "Nomor induk siswa nasional", "fa-hashtag", "text", None, None
    ),
    "nis": ProfileFieldConfig(
        "NIS", "Nomor induk sekolah", "fa-hashtag", "text", None, None
    ),
    "class_level": ProfileFieldConfig(
        "Kelas",
        "Pilih kelas",
        "fa-graduation-cap",
        "choice",
        None,
        "get_class_level_display",
    ),
    "major": ProfileFieldConfig(
        "Jurusan", "Jurusan/Program", "fa-layer-group", "text", None, None
    ),
    "parent_name": ProfileFieldConfig(
        "Nama Orang Tua", "Nama orang tua/wali", "fa-user-tie", "text", None, None
    ),
    "parent_phone": ProfileFieldConfig(
        "Nomor Telepon Orang Tua", "08xxxxxxxxxx", "fa-phone", "text", None, None
    ),
    "nuptk": ProfileFieldConfig(
        "NUPTK", "Nomor unik pendidik", "fa-id-card", "text", None, None
    ),
    "subject": ProfileFieldConfig(
        "Mata Pelajaran",
        "Pilih mata pelajaran",
        "fa-chalkboard-user",
        "choice",
        None,
        "get_subject_display",
    ),
    "position": ProfileFieldConfig(
        "Posisi", "Jabatan/posisi", "fa-briefcase", "text", None, None
    ),
    "institution": ProfileFieldConfig(
        "Institusi", "Nama institusi", "fa-building", "text", None, None
    ),
    "nip": ProfileFieldConfig(
        "NIP", "Nomor induk pegawai", "fa-id-badge", "text", None, None
    ),
    "employee_id": ProfileFieldConfig(
        "ID Pegawai", "ID kepegawaian", "fa-id-card", "text", None, None
    ),
    "bio": ProfileFieldConfig(
        "Biografi Singkat",
        "Deskripsi singkat tentang Anda",
        "fa-align-left",
        "text",
        None,
        None,
    ),
    "website": ProfileFieldConfig(
        "Situs Pribadi", "https://...", "fa-globe", "text", None, None
    ),
    "github": ProfileFieldConfig(
        "GitHub",
        "https://github.com/username",
        "fa-brands fa-github",
        "text",
        None,
        None,
    ),
    "stack_overflow": ProfileFieldConfig(
        "Stack Overflow",
        "https://stackoverflow.com/users/...",
        "fa-brands fa-stack-overflow",
        "text",
        None,
        None,
    ),
    "department": ProfileFieldConfig(
        "Divisi/Bagian", "Divisi/bagian", "fa-building", "text", None, None
    ),
    "fax": ProfileFieldConfig(
        "Nomor Fax", "Nomor fax kantor", "fa-fax", "text", None, None
    ),
    "employee_status": ProfileFieldConfig(
        "Status Kepegawaian",
        "Pilih status",
        "fa-id-card",
        "choice",
        None,
        "get_employee_status_display",
    ),
    "start_date": ProfileFieldConfig(
        "Tanggal Mulai Bekerja", "YYYY-MM-DD", "fa-calendar", "date", None, None
    ),
    "education_background": ProfileFieldConfig(
        "Pendidikan Terakhir", "S1/S2/S3", "fa-graduation-cap", "text", None, None
    ),
    "years_of_experience": ProfileFieldConfig(
        "Pengalaman Mengajar", "Lama pengalaman", "fa-clock", "unit", "tahun", None
    ),
    "certification": ProfileFieldConfig(
        "Sertifikasi Pendidik",
        "Jenis sertifikasi",
        "fa-certificate",
        "text",
        None,
        None,
    ),
    "academic_degree": ProfileFieldConfig(
        "Gelar Akademik", "S.Pd, M.Pd, dll", "fa-user-graduate", "text", None, None
    ),
    "nik": ProfileFieldConfig(
        "NIK", "Nomor induk kependudukan", "fa-id-card", "text", None, None
    ),
    "blood_type": ProfileFieldConfig(
        "Golongan Darah",
        "Pilih golongan darah",
        "fa-droplet",
        "choice",
        None,
        "get_blood_type_display",
    ),
    "height": ProfileFieldConfig(
        "Tinggi Badan", "Tinggi badan", "fa-ruler", "unit", "cm", None
    ),
    "weight": ProfileFieldConfig(
        "Berat Badan", "Berat badan", "fa-weight-scale", "unit", "kg", None
    ),
    "hobby": ProfileFieldConfig(
        "Hobi", "Hobi/kegemaran", "fa-heart", "text", None, None
    ),
    "previous_school": ProfileFieldConfig(
        "Asal Sekolah", "Asal sekolah sebelumnya", "fa-school", "text", None, None
    ),
    "graduation_year": ProfileFieldConfig(
        "Tahun Lulus", "Tahun lulus", "fa-calendar", "text", None, None
    ),
    "counselor": ProfileFieldConfig(
        "Guru BK/Wali", "Nama guru BK/wali", "fa-user-tie", "text", None, None
    ),
    "scholarship_status": ProfileFieldConfig(
        "Status Beasiswa",
        "Pilih status",
        "fa-award",
        "choice",
        None,
        "get_scholarship_status_display",
    ),
    "transportation": ProfileFieldConfig(
        "Transportasi", "Moda transportasi", "fa-bus", "text", None, None
    ),
    "father_name": ProfileFieldConfig(
        "Nama Ayah", "Nama ayah", "fa-user", "text", None, None
    ),
    "mother_name": ProfileFieldConfig(
        "Nama Ibu", "Nama ibu", "fa-user", "text", None, None
    ),
    "father_phone": ProfileFieldConfig(
        "Telepon Ayah", "08xxxxxxxxxx", "fa-phone", "text", None, None
    ),
    "mother_phone": ProfileFieldConfig(
        "Telepon Ibu", "08xxxxxxxxxx", "fa-phone", "text", None, None
    ),
    "parent_address": ProfileFieldConfig(
        "Alamat Orang Tua",
        "Alamat orang tua/wali",
        "fa-location-dot",
        "text",
        None,
        None,
    ),
    "guardian_name": ProfileFieldConfig(
        "Nama Wali", "Nama wali (jika berbeda)", "fa-user-tie", "text", None, None
    ),
}

PROFILE_FIELD_LAYOUT = {
    "address": "pf-field--full",
    "bio": "pf-field--full",
    "education_background": "pf-field--full",
    "parent_address": "pf-field--full",
    "height": "pf-field--quarter",
    "weight": "pf-field--quarter",
    "years_of_experience": "pf-field--quarter",
    "blood_type": "pf-field--quarter",
    "graduation_year": "pf-field--quarter",
    "start_date": "pf-field--third",
    "birth_date": "pf-field--third",
    "gender": "pf-field--third",
    "religion": "pf-field--third",
    "class_level": "pf-field--third",
    "photo": "pf-field--full",
    "code": "pf-field--full",
    "phone": "pf-field--half",
}
