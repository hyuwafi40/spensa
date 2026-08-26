from django.urls import path
from core.views.index import (
    IndexRedirectView,
    DeveloperDashboardView,
    AdministratorDashboardView,
    TeacherDashboardView,
    StudentDashboardView,
)

app_name = "core"

urlpatterns = [
    path("", IndexRedirectView.as_view(), name="index"),
    path("dashboard/developer/", DeveloperDashboardView.as_view(), name="dashboard_developer"),
    path("dashboard/administrator/", AdministratorDashboardView.as_view(), name="dashboard_administrator"),
    path("dashboard/teacher/", TeacherDashboardView.as_view(), name="dashboard_teacher"),
    path("dashboard/student/", StudentDashboardView.as_view(), name="dashboard_student"),
]
