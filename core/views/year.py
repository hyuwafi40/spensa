from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.forms.year import YearForm
from core.models.academic import Year
from core.utils.constants import JobChoices
from core.views.base import RoleDashboardMixin, ElidedPaginationMixin


class YearListView(RoleDashboardMixin, ElidedPaginationMixin, ListView):
    model = Year
    template_name = "core/year.html"
    paginate_by = 10
    roles = [JobChoices.DEVELOPER, JobChoices.ADMINISTRATOR]

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get("q", "").strip()
        if q:
            queryset = queryset.filter(start_year__icontains=q) | queryset.filter(
                finish_year__icontains=q
            )
        return queryset.order_by("start_year")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb_items"] = [
            {"label": "Home", "url": reverse_lazy("core:index")},
            {"label": "Tahun Ajaran", "url": None},
        ]
        return context


class YearCreateView(RoleDashboardMixin, CreateView):
    model = Year
    form_class = YearForm
    template_name = "core/year/form.html"
    success_url = reverse_lazy("core:academic_year")
    roles = [JobChoices.DEVELOPER, JobChoices.ADMINISTRATOR]

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f"Tahun ajaran {self.object.start_year}/{self.object.finish_year} berhasil dibuat.",
        )
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb_items"] = [
            {"label": "Home", "url": reverse_lazy("core:index")},
            {"label": "Tahun Ajaran", "url": reverse_lazy("core:academic_year")},
            {"label": "Tambah", "url": None},
        ]
        return context


class YearUpdateView(RoleDashboardMixin, UpdateView):
    model = Year
    form_class = YearForm
    template_name = "core/year/form.html"
    success_url = reverse_lazy("core:academic_year")
    roles = [JobChoices.DEVELOPER, JobChoices.ADMINISTRATOR]

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f"Tahun ajaran {self.object.start_year}/{self.object.finish_year} berhasil diperbarui.",
        )
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb_items"] = [
            {"label": "Home", "url": reverse_lazy("core:index")},
            {"label": "Tahun Ajaran", "url": reverse_lazy("core:academic_year")},
            {"label": "Edit", "url": None},
        ]
        return context


class YearDeleteView(RoleDashboardMixin, DeleteView):
    model = Year
    success_url = reverse_lazy("core:academic_year")
    roles = [JobChoices.DEVELOPER, JobChoices.ADMINISTRATOR]

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        try:
            response = super().delete(request, *args, **kwargs)
            messages.success(
                request,
                f"Tahun ajaran {obj.start_year}/{obj.finish_year} berhasil dihapus.",
            )
            return response
        except ProtectedError:
            messages.error(
                request,
                f"Tahun ajaran {obj.start_year}/{obj.finish_year} tidak dapat dihapus karena masih digunakan.",
            )
            return redirect(self.success_url)
