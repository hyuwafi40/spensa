from django import forms
from core.forms.base import StyledFormMixin
from core.models.brand import School


class SchoolForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = School
        fields = [
            "name",
            "address",
            "phone",
            "email",
            "website",
            "logo",
            "npsn",
            "nss",
            "accreditation",
            "school_type",
            "status",
            "headmaster_name",
            "headmaster_nip",
            "established_year",
            "fax",
            "postal_code",
            "province",
            "city",
            "district",
            "village",
            "curriculum",
            "since",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            "name": "Nama sekolah",
            "address": "Alamat lengkap",
            "phone": "Nomor telepon",
            "email": "Alamat email",
            "website": "URL website",
            "logo": "URL logo",
            "npsn": "NPSN",
            "nss": "NSS",
            "accreditation": "Akreditasi",
            "school_type": "Jenis sekolah",
            "status": "Status",
            "headmaster_name": "Nama kepala sekolah",
            "headmaster_nip": "NIP kepala sekolah",
            "established_year": "Tahun berdiri",
            "fax": "Nomor fax",
            "postal_code": "Kode pos",
            "province": "Provinsi",
            "city": "Kota/Kabupaten",
            "district": "Kecamatan",
            "village": "Desa/Kelurahan",
            "curriculum": "Kurikulum",
            "since": "Tahun ajaran sejak",
        }
        for field_name, placeholder in placeholders.items():
            if field_name in self.fields:
                self.fields[field_name].widget.attrs["placeholder"] = placeholder
