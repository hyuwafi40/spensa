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


class ElidedPaginationMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context.get("paginator")
        page_obj = context.get("page_obj")
        if paginator and page_obj:
            context["page_range_elided"] = paginator.get_elided_page_range(
                number=page_obj.number,
                on_each_side=1,
                on_ends=1,
            )
        return context
