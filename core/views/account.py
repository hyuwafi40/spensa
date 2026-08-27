from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.forms.account import CustomUserForm
from core.models.account import CustomUser
from core.utils.constants import JobChoices
from core.views.base import RoleDashboardMixin, ElidedPaginationMixin


class AccountListView(RoleDashboardMixin, ElidedPaginationMixin, ListView):
    model = CustomUser
    template_name = "core/account.html"
    paginate_by = 10
    roles = [JobChoices.DEVELOPER, JobChoices.ADMINISTRATOR]

    def get_queryset(self):
        queryset = super().get_queryset().select_related("profile")
        queryset = queryset.exclude(job=JobChoices.DEVELOPER)
        q = self.request.GET.get("q", "").strip()
        if q:
            queryset = (
                queryset.filter(username__icontains=q)
                | queryset.filter(first_name__icontains=q)
                | queryset.filter(last_name__icontains=q)
                | queryset.filter(email__icontains=q)
            )
        return queryset.order_by("username")


class AccountCreateView(RoleDashboardMixin, CreateView):
    model = CustomUser
    form_class = CustomUserForm
    template_name = "core/account/form.html"
    success_url = reverse_lazy("core:user_account")
    roles = [JobChoices.DEVELOPER, JobChoices.ADMINISTRATOR]

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Akun {self.object.username} berhasil dibuat.")
        return response


class AccountUpdateView(RoleDashboardMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserForm
    template_name = "core/account/form.html"
    success_url = reverse_lazy("core:user_account")
    roles = [JobChoices.DEVELOPER, JobChoices.ADMINISTRATOR]

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request, f"Akun {self.object.username} berhasil diperbarui."
        )
        return response


class AccountDeleteView(RoleDashboardMixin, DeleteView):
    model = CustomUser
    success_url = reverse_lazy("core:user_account")
    roles = [JobChoices.DEVELOPER, JobChoices.ADMINISTRATOR]

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        if user == request.user:
            messages.error(request, "Anda tidak dapat menghapus akun sendiri.")
            return redirect(self.success_url)
        if user.is_superuser and not request.user.is_superuser:
            messages.error(request, "Hanya developer yang dapat menghapus superuser.")
            return redirect(self.success_url)
        try:
            response = super().delete(request, *args, **kwargs)
            messages.success(request, f"Akun {user.username} berhasil dihapus.")
            return response
        except ProtectedError:
            messages.error(
                request,
                f"Akun {user.username} tidak dapat dihapus karena masih memiliki data terkait.",
            )
            return redirect(self.success_url)


class AccountResetPasswordView(RoleDashboardMixin, View):
    roles = [JobChoices.DEVELOPER, JobChoices.ADMINISTRATOR]

    def post(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        default_password = "baskara123"
        user.set_password(default_password)
        user.save()
        messages.success(
            request, f"Password {user.username} berhasil direset ke {default_password}."
        )
        return redirect("core:user_account")
