from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views import View
from core.utils.security import (
    clear_login_attempts,
    is_login_blocked,
    record_failed_login,
)


class IndexView(View):
    template_name = "index.html"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("core:index")
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")

        if is_login_blocked(request, username):
            messages.error(
                request,
                "Terlalu banyak percobaan login. Silakan coba lagi dalam 5 menit.",
            )
            return render(request, self.template_name)

        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            clear_login_attempts(request, username)
            messages.success(
                request, f"Selamat datang, {user.get_full_name() or user.username}!"
            )
            next_url = request.POST.get("next") or request.GET.get("next")
            if next_url and url_has_allowed_host_and_scheme(
                url=next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure(),
            ):
                return redirect(next_url)
            return redirect("core:index")
        if user is not None and not user.is_active:
            messages.error(request, "Akun Anda telah dinonaktifkan.")
        else:
            record_failed_login(request, username)
            messages.error(request, "Username atau Password salah!")
        return render(request, self.template_name)


def logout_view(request):
    if request.method == "POST":
        logout(request)
        messages.info(request, "Anda telah keluar.")
    return redirect("login")
