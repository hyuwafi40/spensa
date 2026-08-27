from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.forms.subject import SubjectForm
from core.models.academic import Subject
from core.utils.constants import JobChoices
from core.views.base import RoleDashboardMixin, ElidedPaginationMixin


class SubjectListView(RoleDashboardMixin, ElidedPaginationMixin, ListView):
    model = Subject
    template_name = "core/subject.html"
    paginate_by = 10
    roles = [JobChoices.DEVELOPER, JobChoices.ADMINISTRATOR]

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get("q", "").strip()
        if q:
            queryset = queryset.filter(code__icontains=q) | queryset.filter(
                name__icontains=q
            )
        return queryset.order_by("code")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb_items"] = [
            {"label": "Home", "url": reverse_lazy("core:index")},
            {"label": "Mata Pelajaran", "url": None},
        ]
        return context


class SubjectCreateView(RoleDashboardMixin, CreateView):
    model = Subject
    form_class = SubjectForm
    template_name = "core/subject/form.html"
    success_url = reverse_lazy("core:subject")
    roles = [JobChoices.DEVELOPER, JobChoices.ADMINISTRATOR]

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request, f"Mata pelajaran {self.object.name} berhasil dibuat."
        )
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb_items"] = [
            {"label": "Home", "url": reverse_lazy("core:index")},
            {"label": "Mata Pelajaran", "url": reverse_lazy("core:subject")},
            {"label": "Tambah", "url": None},
        ]
        return context


class SubjectUpdateView(RoleDashboardMixin, UpdateView):
    model = Subject
    form_class = SubjectForm
    template_name = "core/subject/form.html"
    success_url = reverse_lazy("core:subject")
    roles = [JobChoices.DEVELOPER, JobChoices.ADMINISTRATOR]

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request, f"Mata pelajaran {self.object.name} berhasil diperbarui."
        )
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb_items"] = [
            {"label": "Home", "url": reverse_lazy("core:index")},
            {"label": "Mata Pelajaran", "url": reverse_lazy("core:subject")},
            {"label": "Edit", "url": None},
        ]
        return context


class SubjectDeleteView(RoleDashboardMixin, DeleteView):
    model = Subject
    success_url = reverse_lazy("core:subject")
    roles = [JobChoices.DEVELOPER, JobChoices.ADMINISTRATOR]

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        try:
            response = super().delete(request, *args, **kwargs)
            messages.success(request, f"Mata pelajaran {obj.name} berhasil dihapus.")
            return response
        except ProtectedError:
            messages.error(
                request,
                f"Mata pelajaran {obj.name} tidak dapat dihapus karena masih digunakan.",
            )
            return redirect(self.success_url)
