from django.urls import path
from core.views.activeyear import (
    ActiveYearListView,
    ActiveYearCreateView,
    ActiveYearUpdateView,
    ActiveYearDeleteView,
    ActiveYearToggleActiveView,
)

urlpatterns = [
    path("active-years/", ActiveYearListView.as_view(), name="active_year"),
    path("active-years/create/", ActiveYearCreateView.as_view(), name="active_year_create"),
    path("active-years/<int:pk>/update/", ActiveYearUpdateView.as_view(), name="active_year_update"),
    path("active-years/<int:pk>/delete/", ActiveYearDeleteView.as_view(), name="active_year_delete"),
    path("active-years/<int:pk>/toggle-active/", ActiveYearToggleActiveView.as_view(), name="active_year_toggle"),
]
