from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.forms.term import TermForm
from core.models.academic import Term
from core.utils.constants import JobChoices
from core.views.base import RoleDashboardMixin, ElidedPaginationMixin


class TermListView(RoleDashboardMixin, ElidedPaginationMixin, ListView):
    model = Term
    template_name = "core/term.html"
    paginate_by = 10
    roles = [JobChoices.DEVELOPER, JobChoices.ADMINISTRATOR]

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get("q", "").strip()
        if q:
            queryset = queryset.filter(name__icontains=q)
        return queryset.order_by("name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb_items"] = [
            {"label": "Home", "url": reverse_lazy("core:index")},
            {"label": "Semester", "url": None},
        ]
        return context


class TermCreateView(RoleDashboardMixin, CreateView):
    model = Term
    form_class = TermForm
    template_name = "core/term/form.html"
    success_url = reverse_lazy("core:term")
    roles = [JobChoices.DEVELOPER, JobChoices.ADMINISTRATOR]

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request, f"Semester {self.object.get_name_display()} berhasil dibuat."
        )
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb_items"] = [
            {"label": "Home", "url": reverse_lazy("core:index")},
            {"label": "Semester", "url": reverse_lazy("core:term")},
            {"label": "Tambah", "url": None},
        ]
        return context


class TermUpdateView(RoleDashboardMixin, UpdateView):
    model = Term
    form_class = TermForm
    template_name = "core/term/form.html"
    success_url = reverse_lazy("core:term")
    roles = [JobChoices.DEVELOPER, JobChoices.ADMINISTRATOR]

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f"Semester {self.object.get_name_display()} berhasil diperbarui.",
        )
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb_items"] = [
            {"label": "Home", "url": reverse_lazy("core:index")},
            {"label": "Semester", "url": reverse_lazy("core:term")},
            {"label": "Edit", "url": None},
        ]
        return context


class TermDeleteView(RoleDashboardMixin, DeleteView):
    model = Term
    success_url = reverse_lazy("core:term")
    roles = [JobChoices.DEVELOPER, JobChoices.ADMINISTRATOR]

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        try:
            response = super().delete(request, *args, **kwargs)
            messages.success(
                request, f"Semester {obj.get_name_display()} berhasil dihapus."
            )
            return response
        except ProtectedError:
            messages.error(
                request,
                f"Semester {obj.get_name_display()} tidak dapat dihapus karena masih digunakan.",
            )
            return redirect(self.success_url)
