from django.urls import path
from core.views.activesubject import (
    ActiveSubjectListView,
    ActiveSubjectCreateView,
    ActiveSubjectUpdateView,
    ActiveSubjectDeleteView,
)

urlpatterns = [
    path("active-subjects/", ActiveSubjectListView.as_view(), name="active_subject"),
    path("active-subjects/create/", ActiveSubjectCreateView.as_view(), name="active_subject_create"),
    path("active-subjects/<int:pk>/update/", ActiveSubjectUpdateView.as_view(), name="active_subject_update"),
    path("active-subjects/<int:pk>/delete/", ActiveSubjectDeleteView.as_view(), name="active_subject_delete"),
]
