from django.contrib import messages
from django.db.models import ProtectedError, Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.forms.activeyear import ActiveYearForm
from core.models.academic import ActiveYear
from core.utils.constants import JobChoices
from core.views.base import RoleDashboardMixin, ElidedPaginationMixin


class ActiveYearListView(RoleDashboardMixin, ElidedPaginationMixin, ListView):
    model = ActiveYear
    template_name = "core/activeyear.html"
    paginate_by = 10
    roles = [JobChoices.DEVELOPER, JobChoices.ADMINISTRATOR]

    def get_queryset(self):
        queryset = super().get_queryset().select_related("year", "term")
        q = self.request.GET.get("q", "").strip()
        if q:
            queryset = queryset.filter(
                Q(year__start_year__icontains=q)
                | Q(year__finish_year__icontains=q)
                | Q(term__name__icontains=q)
            )
        return queryset.order_by("-is_active", "year__start_year")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb_items"] = [
            {"label": "Home", "url": reverse_lazy("core:index")},
            {"label": "Tahun Ajaran Aktif", "url": None},
        ]
        return context


class ActiveYearCreateView(RoleDashboardMixin, CreateView):
    model = ActiveYear
    form_class = ActiveYearForm
    template_name = "core/activeyear/form.html"
    success_url = reverse_lazy("core:active_year")
    roles = [JobChoices.DEVELOPER, JobChoices.ADMINISTRATOR]

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f"Tahun ajaran aktif {self.object.year} - {self.object.term.get_name_display()} berhasil dibuat.",
        )
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb_items"] = [
            {"label": "Home", "url": reverse_lazy("core:index")},
            {"label": "Tahun Ajaran Aktif", "url": reverse_lazy("core:active_year")},
            {"label": "Tambah", "url": None},
        ]
        return context


class ActiveYearUpdateView(RoleDashboardMixin, UpdateView):
    model = ActiveYear
    form_class = ActiveYearForm
    template_name = "core/activeyear/form.html"
    success_url = reverse_lazy("core:active_year")
    roles = [JobChoices.DEVELOPER, JobChoices.ADMINISTRATOR]

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f"Tahun ajaran aktif {self.object.year} - {self.object.term.get_name_display()} berhasil diperbarui.",
        )
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb_items"] = [
            {"label": "Home", "url": reverse_lazy("core:index")},
            {"label": "Tahun Ajaran Aktif", "url": reverse_lazy("core:active_year")},
            {"label": "Edit", "url": None},
        ]
        return context


class ActiveYearDeleteView(RoleDashboardMixin, DeleteView):
    model = ActiveYear
    success_url = reverse_lazy("core:active_year")
    roles = [JobChoices.DEVELOPER, JobChoices.ADMINISTRATOR]

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        try:
            response = super().delete(request, *args, **kwargs)
            messages.success(
                request,
                f"Tahun ajaran aktif {obj.year} - {obj.term.get_name_display()} berhasil dihapus.",
            )
            return response
        except ProtectedError:
            messages.error(
                request,
                f"Tahun ajaran aktif {obj.year} - {obj.term.get_name_display()} tidak dapat dihapus karena masih digunakan.",
            )
            return redirect(self.success_url)


class ActiveYearToggleActiveView(RoleDashboardMixin, View):
    roles = [JobChoices.DEVELOPER, JobChoices.ADMINISTRATOR]

    def post(self, request, pk):
        obj = get_object_or_404(ActiveYear, pk=pk)
        obj.is_active = not obj.is_active
        obj.save()
        status = "diaktifkan" if obj.is_active else "dinonaktifkan"
        messages.success(
            request,
            f"Tahun ajaran aktif {obj.year} - {obj.term.get_name_display()} berhasil {status}.",
        )
        return redirect("core:active_year")
