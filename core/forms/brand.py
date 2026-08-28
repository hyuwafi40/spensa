from django import forms
from core.forms.base import StyledFormMixin
from core.models.brand import Brand


class BrandForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Brand
        fields = [
            "name",
            "description",
            "version",
            "tahun",
            "logo",
            "instagram",
            "youtube",
            "tiktok",
            "facebook",
            "developer",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            "name": "Nama brand",
            "description": "Deskripsi singkat",
            "version": "Versi aplikasi",
            "tahun": "Tahun rilis",
            "logo": "URL logo",
            "instagram": "URL Instagram",
            "youtube": "URL YouTube",
            "tiktok": "URL TikTok",
            "facebook": "URL Facebook",
            "developer": "Nama pengembang",
        }
        for field_name, placeholder in placeholders.items():
            if field_name in self.fields:
                self.fields[field_name].widget.attrs["placeholder"] = placeholder
