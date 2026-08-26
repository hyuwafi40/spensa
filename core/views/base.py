from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from core.access import has_role


class RoleDashboardMixin(LoginRequiredMixin):
    template_name = None
    roles = []

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        if not request.user.is_active:
            raise PermissionDenied
        if not has_role(request.user, *self.roles):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
