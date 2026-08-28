from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView
from core.models.log import DeveloperLog
from core.utils.constants import JobChoices
from core.views.base import RoleDashboardMixin, ElidedPaginationMixin


class LogListView(RoleDashboardMixin, ElidedPaginationMixin, ListView):
    model = DeveloperLog
    template_name = "core/log.html"
    paginate_by = 10
    roles = [JobChoices.DEVELOPER, JobChoices.ADMINISTRATOR]

    def get_queryset(self):
        queryset = super().get_queryset().select_related("user")
        q = self.request.GET.get("q", "").strip()
        if q:
            queryset = queryset.filter(
                Q(level__icontains=q)
                | Q(event__icontains=q)
                | Q(path__icontains=q)
                | Q(method__icontains=q)
                | Q(status_code__icontains=q)
                | Q(module__icontains=q)
                | Q(action__icontains=q)
                | Q(object_repr__icontains=q)
                | Q(user__username__icontains=q)
                | Q(ip_address__icontains=q)
            )
        return queryset.order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb_items"] = [
            {"label": "Home", "url": reverse_lazy("core:index")},
            {"label": "Log Aktivitas", "url": None},
        ]
        return context
