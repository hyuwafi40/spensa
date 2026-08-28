from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView
from core.forms.school import SchoolForm
from core.models.brand import School
from core.utils.constants import JobChoices
from core.views.base import RoleDashboardMixin


class SchoolPageView(RoleDashboardMixin, TemplateView):
    template_name = "core/school.html"
    roles = [JobChoices.DEVELOPER, JobChoices.ADMINISTRATOR]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school = School.get_solo()
        context["school"] = school
        context["has_school"] = bool(school.name)
        context["breadcrumb_items"] = [
            {"label": "Home", "url": reverse_lazy("core:index")},
            {"label": "Sekolah", "url": None},
        ]
        return context


class SchoolCreateView(RoleDashboardMixin, UpdateView):
    model = School
    form_class = SchoolForm
    template_name = "core/school/form.html"
    success_url = reverse_lazy("core:school")
    roles = [JobChoices.DEVELOPER, JobChoices.ADMINISTRATOR]

    def get_object(self, queryset=None):
        return School.get_solo()

    def dispatch(self, request, *args, **kwargs):
        school = School.get_solo()
        if school.name:
            return redirect("core:school_update")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Data sekolah berhasil dibuat.")
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb_items"] = [
            {"label": "Home", "url": reverse_lazy("core:index")},
            {"label": "Sekolah", "url": reverse_lazy("core:school")},
            {"label": "Tambah", "url": None},
        ]
        return context


class SchoolUpdateView(RoleDashboardMixin, UpdateView):
    model = School
    form_class = SchoolForm
    template_name = "core/school/form.html"
    success_url = reverse_lazy("core:school")
    roles = [JobChoices.DEVELOPER, JobChoices.ADMINISTRATOR]

    def get_object(self, queryset=None):
        return School.get_solo()

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Data sekolah berhasil diperbarui.")
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb_items"] = [
            {"label": "Home", "url": reverse_lazy("core:index")},
            {"label": "Sekolah", "url": reverse_lazy("core:school")},
            {"label": "Edit", "url": None},
        ]
        return context
