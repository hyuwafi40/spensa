from django.urls import path
from core.views.subject import (
    SubjectListView,
    SubjectCreateView,
    SubjectUpdateView,
    SubjectDeleteView,
)

urlpatterns = [
    path("subjects/", SubjectListView.as_view(), name="subject"),
    path("subjects/create/", SubjectCreateView.as_view(), name="subject_create"),
    path("subjects/<int:pk>/update/", SubjectUpdateView.as_view(), name="subject_update"),
    path("subjects/<int:pk>/delete/", SubjectDeleteView.as_view(), name="subject_delete"),
]
