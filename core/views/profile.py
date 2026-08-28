from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView
from core.forms.profile import UserProfileForm, ProfileDetailForm
from core.models.account import Profile
from core.utils.fields import get_profile_fields


class ProfilePageView(LoginRequiredMixin, TemplateView):
    template_name = "core/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        profile = Profile.objects.filter(user=user).first()
        context["user"] = user
        context["profile"] = profile
        context["has_profile"] = profile is not None
        context["profile_fields"] = get_profile_fields(user, profile)
        context["breadcrumb_items"] = [
            {"label": "Home", "url": reverse_lazy("core:index")},
            {"label": "Profil", "url": None},
        ]
        return context


class ProfileUpdateView(LoginRequiredMixin, View):
    template_name = "core/profile/form.html"
    success_url = reverse_lazy("core:profile")

    def get(self, request, *args, **kwargs):
        user = request.user
        profile = Profile.objects.filter(user=user).first()
        user_form = UserProfileForm(instance=user)
        profile_form = ProfileDetailForm(instance=profile, role=user.job)
        context = {
            "user_form": user_form,
            "profile_form": profile_form,
            "breadcrumb_items": [
                {"label": "Home", "url": reverse_lazy("core:index")},
                {"label": "Profil", "url": self.success_url},
                {"label": "Edit", "url": None},
            ],
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user = request.user
        profile = Profile.objects.filter(user=user).first()
        user_form = UserProfileForm(request.POST, instance=user)
        profile_form = ProfileDetailForm(request.POST, instance=profile, role=user.job)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_obj = profile_form.save(commit=False)
            profile_obj.user = user
            profile_obj.save()
            messages.success(request, "Profil berhasil diperbarui.")
            return redirect(self.success_url)

        context = {
            "user_form": user_form,
            "profile_form": profile_form,
            "breadcrumb_items": [
                {"label": "Home", "url": reverse_lazy("core:index")},
                {"label": "Profil", "url": self.success_url},
                {"label": "Edit", "url": None},
            ],
        }
        return render(request, self.template_name, context)
