from django.urls import path
from core.views.term import (
    TermListView,
    TermCreateView,
    TermUpdateView,
    TermDeleteView,
)

urlpatterns = [
    path("terms/", TermListView.as_view(), name="term"),
    path("terms/create/", TermCreateView.as_view(), name="term_create"),
    path("terms/<int:pk>/update/", TermUpdateView.as_view(), name="term_update"),
    path("terms/<int:pk>/delete/", TermDeleteView.as_view(), name="term_delete"),
]
