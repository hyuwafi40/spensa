from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.forms.classroom import ClassroomForm
from core.models.academic import Classroom
from core.utils.constants import JobChoices
from core.views.base import RoleDashboardMixin, ElidedPaginationMixin


class ClassroomListView(RoleDashboardMixin, ElidedPaginationMixin, ListView):
    model = Classroom
    template_name = "core/classroom.html"
    paginate_by = 10
    roles = [JobChoices.DEVELOPER, JobChoices.ADMINISTRATOR]

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get("q", "").strip()
        if q:
            queryset = queryset.filter(name__icontains=q) | queryset.filter(
                grade__icontains=q
            )
        return queryset.order_by("grade", "name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb_items"] = [
            {"label": "Home", "url": reverse_lazy("core:index")},
            {"label": "Kelas", "url": None},
        ]
        return context


class ClassroomCreateView(RoleDashboardMixin, CreateView):
    model = Classroom
    form_class = ClassroomForm
    template_name = "core/classroom/form.html"
    success_url = reverse_lazy("core:classroom")
    roles = [JobChoices.DEVELOPER, JobChoices.ADMINISTRATOR]

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f"Kelas {self.object.get_grade_display()} - {self.object.name} berhasil dibuat.",
        )
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb_items"] = [
            {"label": "Home", "url": reverse_lazy("core:index")},
            {"label": "Kelas", "url": reverse_lazy("core:classroom")},
            {"label": "Tambah", "url": None},
        ]
        return context


class ClassroomUpdateView(RoleDashboardMixin, UpdateView):
    model = Classroom
    form_class = ClassroomForm
    template_name = "core/classroom/form.html"
    success_url = reverse_lazy("core:classroom")
    roles = [JobChoices.DEVELOPER, JobChoices.ADMINISTRATOR]

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f"Kelas {self.object.get_grade_display()} - {self.object.name} berhasil diperbarui.",
        )
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb_items"] = [
            {"label": "Home", "url": reverse_lazy("core:index")},
            {"label": "Kelas", "url": reverse_lazy("core:classroom")},
            {"label": "Edit", "url": None},
        ]
        return context


class ClassroomDeleteView(RoleDashboardMixin, DeleteView):
    model = Classroom
    success_url = reverse_lazy("core:classroom")
    roles = [JobChoices.DEVELOPER, JobChoices.ADMINISTRATOR]

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        try:
            response = super().delete(request, *args, **kwargs)
            messages.success(
                request,
                f"Kelas {obj.get_grade_display()} - {obj.name} berhasil dihapus.",
            )
            return response
        except ProtectedError:
            messages.error(
                request,
                f"Kelas {obj.get_grade_display()} - {obj.name} tidak dapat dihapus karena masih digunakan.",
            )
            return redirect(self.success_url)
