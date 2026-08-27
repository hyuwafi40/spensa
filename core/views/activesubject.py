from django.contrib import messages
from django.db.models import ProtectedError, Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.forms.activesubject import ActiveSubjectForm
from core.models.academic import ActiveSubject
from core.utils.constants import JobChoices
from core.views.base import RoleDashboardMixin, ElidedPaginationMixin


class ActiveSubjectListView(RoleDashboardMixin, ElidedPaginationMixin, ListView):
    model = ActiveSubject
    template_name = "core/activesubject.html"
    paginate_by = 10
    roles = [JobChoices.DEVELOPER, JobChoices.ADMINISTRATOR]

    def get_queryset(self):
        queryset = (
            super()
            .get_queryset()
            .select_related(
                "active_year__year",
                "active_year__term",
                "subject",
                "classroom",
                "teacher",
            )
        )
        q = self.request.GET.get("q", "").strip()
        if q:
            queryset = queryset.filter(
                Q(active_year__year__start_year__icontains=q)
                | Q(active_year__year__finish_year__icontains=q)
                | Q(active_year__term__name__icontains=q)
                | Q(subject__code__icontains=q)
                | Q(subject__name__icontains=q)
                | Q(classroom__name__icontains=q)
                | Q(teacher__username__icontains=q)
                | Q(teacher__first_name__icontains=q)
                | Q(teacher__last_name__icontains=q)
            )
        return queryset.order_by("active_year__year__start_year", "subject__name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb_items"] = [
            {"label": "Home", "url": reverse_lazy("core:index")},
            {"label": "Mata Pelajaran Aktif", "url": None},
        ]
        return context


class ActiveSubjectCreateView(RoleDashboardMixin, CreateView):
    model = ActiveSubject
    form_class = ActiveSubjectForm
    template_name = "core/activesubject/form.html"
    success_url = reverse_lazy("core:active_subject")
    roles = [JobChoices.DEVELOPER, JobChoices.ADMINISTRATOR]

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f"Mata pelajaran aktif {self.object.subject.name} berhasil dibuat.",
        )
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb_items"] = [
            {"label": "Home", "url": reverse_lazy("core:index")},
            {
                "label": "Mata Pelajaran Aktif",
                "url": reverse_lazy("core:active_subject"),
            },
            {"label": "Tambah", "url": None},
        ]
        return context


class ActiveSubjectUpdateView(RoleDashboardMixin, UpdateView):
    model = ActiveSubject
    form_class = ActiveSubjectForm
    template_name = "core/activesubject/form.html"
    success_url = reverse_lazy("core:active_subject")
    roles = [JobChoices.DEVELOPER, JobChoices.ADMINISTRATOR]

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f"Mata pelajaran aktif {self.object.subject.name} berhasil diperbarui.",
        )
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb_items"] = [
            {"label": "Home", "url": reverse_lazy("core:index")},
            {
                "label": "Mata Pelajaran Aktif",
                "url": reverse_lazy("core:active_subject"),
            },
            {"label": "Edit", "url": None},
        ]
        return context


class ActiveSubjectDeleteView(RoleDashboardMixin, DeleteView):
    model = ActiveSubject
    success_url = reverse_lazy("core:active_subject")
    roles = [JobChoices.DEVELOPER, JobChoices.ADMINISTRATOR]

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        try:
            response = super().delete(request, *args, **kwargs)
            messages.success(
                request, f"Mata pelajaran aktif {obj.subject.name} berhasil dihapus."
            )
            return response
        except ProtectedError:
            messages.error(
                request,
                f"Mata pelajaran aktif {obj.subject.name} tidak dapat dihapus karena masih digunakan.",
            )
            return redirect(self.success_url)
