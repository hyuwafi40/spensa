from django.urls import path
from core.views.school import SchoolPageView, SchoolCreateView, SchoolUpdateView

urlpatterns = [
    path("school/", SchoolPageView.as_view(), name="school"),
    path("school/create/", SchoolCreateView.as_view(), name="school_create"),
    path("school/update/", SchoolUpdateView.as_view(), name="school_update"),
]
