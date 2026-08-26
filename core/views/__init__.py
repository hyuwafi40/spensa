from .index import (
    IndexRedirectView,
    DeveloperDashboardView,
    AdministratorDashboardView,
    TeacherDashboardView,
    StudentDashboardView,
)
from .account import (
    AccountListView,
    AccountCreateView,
    AccountUpdateView,
    AccountDeleteView,
    AccountResetPasswordView,
)

__all__ = [
    "IndexRedirectView",
    "DeveloperDashboardView",
    "AdministratorDashboardView",
    "TeacherDashboardView",
    "StudentDashboardView",
    "AccountListView",
    "AccountCreateView",
    "AccountUpdateView",
    "AccountDeleteView",
    "AccountResetPasswordView",
]
