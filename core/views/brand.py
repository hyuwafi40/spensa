from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView
from core.forms.brand import BrandForm
from core.models.brand import Brand
from core.utils.constants import JobChoices
from core.views.base import RoleDashboardMixin


class BrandPageView(RoleDashboardMixin, TemplateView):
    template_name = "core/brand.html"
    roles = [JobChoices.DEVELOPER]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        brand = Brand.get_solo()
        context["brand"] = brand
        context["has_brand"] = bool(brand.name)
        context["breadcrumb_items"] = [
            {"label": "Home", "url": reverse_lazy("core:index")},
            {"label": "Brand", "url": None},
        ]
        return context


class BrandCreateView(RoleDashboardMixin, UpdateView):
    model = Brand
    form_class = BrandForm
    template_name = "core/brand/form.html"
    success_url = reverse_lazy("core:brand")
    roles = [JobChoices.DEVELOPER]

    def get_object(self, queryset=None):
        return Brand.get_solo()

    def dispatch(self, request, *args, **kwargs):
        brand = Brand.get_solo()
        if brand.name:
            return redirect("core:brand_update")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Brand berhasil dibuat.")
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb_items"] = [
            {"label": "Home", "url": reverse_lazy("core:index")},
            {"label": "Brand", "url": reverse_lazy("core:brand")},
            {"label": "Tambah", "url": None},
        ]
        return context


class BrandUpdateView(RoleDashboardMixin, UpdateView):
    model = Brand
    form_class = BrandForm
    template_name = "core/brand/form.html"
    success_url = reverse_lazy("core:brand")
    roles = [JobChoices.DEVELOPER]

    def get_object(self, queryset=None):
        return Brand.get_solo()

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Brand berhasil diperbarui.")
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb_items"] = [
            {"label": "Home", "url": reverse_lazy("core:index")},
            {"label": "Brand", "url": reverse_lazy("core:brand")},
            {"label": "Edit", "url": None},
        ]
        return context
