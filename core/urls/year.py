from django.urls import path
from core.views.year import (
    YearListView,
    YearCreateView,
    YearUpdateView,
    YearDeleteView,
)

urlpatterns = [
    path("academic-years/", YearListView.as_view(), name="academic_year"),
    path("academic-years/create/", YearCreateView.as_view(), name="year_create"),
    path("academic-years/<int:pk>/update/", YearUpdateView.as_view(), name="year_update"),
    path("academic-years/<int:pk>/delete/", YearDeleteView.as_view(), name="year_delete"),
]
