from django.contrib import messages
from django.db.models import ProtectedError, Q, Count
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.forms.activeclassroom import ActiveClassroomForm, ActiveStudentForm
from core.models.academic import ActiveClassroom, ActiveStudent
from core.utils.constants import JobChoices
from core.views.base import RoleDashboardMixin, ElidedPaginationMixin


class ActiveClassroomListView(RoleDashboardMixin, ElidedPaginationMixin, ListView):
    model = ActiveClassroom
    template_name = "core/activeclassroom.html"
    paginate_by = 10
    roles = [JobChoices.DEVELOPER, JobChoices.ADMINISTRATOR]

    def get_queryset(self):
        queryset = (
            super()
            .get_queryset()
            .select_related(
                "active_year__year",
                "active_year__term",
                "classroom",
                "teacher",
            )
            .annotate(student_count=Count("active_students"))
        )
        q = self.request.GET.get("q", "").strip()
        if q:
            queryset = queryset.filter(
                Q(active_year__year__start_year__icontains=q)
                | Q(active_year__year__finish_year__icontains=q)
                | Q(active_year__term__name__icontains=q)
                | Q(classroom__name__icontains=q)
                | Q(teacher__username__icontains=q)
                | Q(teacher__first_name__icontains=q)
                | Q(teacher__last_name__icontains=q)
            )
        return queryset.order_by("-active_year__year__start_year", "classroom__name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb_items"] = [
            {"label": "Home", "url": reverse_lazy("core:index")},
            {"label": "Kelas Aktif", "url": None},
        ]
        return context


class ActiveClassroomCreateView(RoleDashboardMixin, CreateView):
    model = ActiveClassroom
    form_class = ActiveClassroomForm
    template_name = "core/activeclassroom/form_cs.html"
    success_url = reverse_lazy("core:active_classroom")
    roles = [JobChoices.DEVELOPER, JobChoices.ADMINISTRATOR]

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request, f"Kelas aktif {self.object.classroom} berhasil dibuat."
        )
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb_items"] = [
            {"label": "Home", "url": reverse_lazy("core:index")},
            {"label": "Kelas Aktif", "url": reverse_lazy("core:active_classroom")},
            {"label": "Tambah", "url": None},
        ]
        return context


class ActiveClassroomUpdateView(RoleDashboardMixin, UpdateView):
    model = ActiveClassroom
    form_class = ActiveClassroomForm
    template_name = "core/activeclassroom/form_cs.html"
    success_url = reverse_lazy("core:active_classroom")
    roles = [JobChoices.DEVELOPER, JobChoices.ADMINISTRATOR]

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request, f"Kelas aktif {self.object.classroom} berhasil diperbarui."
        )
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb_items"] = [
            {"label": "Home", "url": reverse_lazy("core:index")},
            {"label": "Kelas Aktif", "url": reverse_lazy("core:active_classroom")},
            {"label": "Edit", "url": None},
        ]
        return context


class ActiveClassroomDeleteView(RoleDashboardMixin, DeleteView):
    model = ActiveClassroom
    template_name = "core/base/delete.html"
    success_url = reverse_lazy("core:active_classroom")
    roles = [JobChoices.DEVELOPER, JobChoices.ADMINISTRATOR]

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        try:
            response = super().delete(request, *args, **kwargs)
            messages.success(request, f"Kelas aktif {obj.classroom} berhasil dihapus.")
            return response
        except ProtectedError:
            messages.error(
                request,
                f"Kelas aktif {obj.classroom} tidak dapat dihapus karena masih memiliki siswa atau data terkait.",
            )
            return redirect(self.success_url)


class ActiveStudentListView(RoleDashboardMixin, ElidedPaginationMixin, ListView):
    model = ActiveStudent
    template_name = "core/activeclassroom/activestudent.html"
    paginate_by = 10
    roles = [JobChoices.DEVELOPER, JobChoices.ADMINISTRATOR]

    def get_classroom(self):
        classroom_id = self.kwargs.get("classroom_id")
        return get_object_or_404(ActiveClassroom, pk=classroom_id)

    def get_queryset(self):
        classroom = self.get_classroom()
        queryset = (
            super()
            .get_queryset()
            .filter(classroom=classroom)
            .select_related(
                "student",
                "classroom__active_year__year",
                "classroom__active_year__term",
            )
        )
        q = self.request.GET.get("q", "").strip()
        if q:
            queryset = queryset.filter(
                Q(student__username__icontains=q)
                | Q(student__first_name__icontains=q)
                | Q(student__last_name__icontains=q)
            )
        return queryset.order_by("student__username")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        classroom = self.get_classroom()
        context["classroom"] = classroom
        context["breadcrumb_items"] = [
            {"label": "Home", "url": reverse_lazy("core:index")},
            {"label": "Kelas Aktif", "url": reverse_lazy("core:active_classroom")},
            {"label": f"Siswa {classroom.classroom}", "url": None},
        ]
        return context


class ActiveStudentCreateView(RoleDashboardMixin, CreateView):
    model = ActiveStudent
    form_class = ActiveStudentForm
    template_name = "core/activeclassroom/form_st.html"
    roles = [JobChoices.DEVELOPER, JobChoices.ADMINISTRATOR]

    def get_classroom(self):
        classroom_id = self.kwargs.get("classroom_id")
        return get_object_or_404(ActiveClassroom, pk=classroom_id)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["classroom"] = self.get_classroom()
        return kwargs

    def get_success_url(self):
        return reverse_lazy(
            "core:active_student_list",
            kwargs={"classroom_id": self.kwargs.get("classroom_id")},
        )

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f"Siswa {self.object.student.get_full_name() or self.object.student.username} berhasil ditambahkan ke kelas.",
        )
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        classroom = self.get_classroom()
        context["classroom"] = classroom
        context["breadcrumb_items"] = [
            {"label": "Home", "url": reverse_lazy("core:index")},
            {"label": "Kelas Aktif", "url": reverse_lazy("core:active_classroom")},
            {
                "label": f"Siswa {classroom.classroom}",
                "url": reverse_lazy(
                    "core:active_student_list", kwargs={"classroom_id": classroom.pk}
                ),
            },
            {"label": "Tambah", "url": None},
        ]
        return context


class ActiveStudentUpdateView(RoleDashboardMixin, UpdateView):
    model = ActiveStudent
    form_class = ActiveStudentForm
    template_name = "core/activeclassroom/form_st.html"
    roles = [JobChoices.DEVELOPER, JobChoices.ADMINISTRATOR]

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        obj = self.get_object()
        kwargs["classroom"] = obj.classroom
        return kwargs

    def get_success_url(self):
        obj = self.get_object()
        return reverse_lazy(
            "core:active_student_list", kwargs={"classroom_id": obj.classroom.pk}
        )

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f"Siswa {self.object.student.get_full_name() or self.object.student.username} berhasil diperbarui.",
        )
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        classroom = obj.classroom
        context["classroom"] = classroom
        context["breadcrumb_items"] = [
            {"label": "Home", "url": reverse_lazy("core:index")},
            {"label": "Kelas Aktif", "url": reverse_lazy("core:active_classroom")},
            {
                "label": f"Siswa {classroom.classroom}",
                "url": reverse_lazy(
                    "core:active_student_list", kwargs={"classroom_id": classroom.pk}
                ),
            },
            {"label": "Edit", "url": None},
        ]
        return context


class ActiveStudentDeleteView(RoleDashboardMixin, DeleteView):
    model = ActiveStudent
    template_name = "core/base/delete.html"
    roles = [JobChoices.DEVELOPER, JobChoices.ADMINISTRATOR]

    def get_success_url(self):
        obj = self.get_object()
        return reverse_lazy(
            "core:active_student_list", kwargs={"classroom_id": obj.classroom.pk}
        )

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        response = super().delete(request, *args, **kwargs)
        messages.success(
            request,
            f"Siswa {obj.student.get_full_name() or obj.student.username} berhasil dihapus dari kelas.",
        )
        return response
