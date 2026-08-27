from django.urls import path
from core.views.classroom import (
    ClassroomListView,
    ClassroomCreateView,
    ClassroomUpdateView,
    ClassroomDeleteView,
)

urlpatterns = [
    path("classrooms/", ClassroomListView.as_view(), name="classroom"),
    path("classrooms/create/", ClassroomCreateView.as_view(), name="classroom_create"),
    path("classrooms/<int:pk>/update/", ClassroomUpdateView.as_view(), name="classroom_update"),
    path("classrooms/<int:pk>/delete/", ClassroomDeleteView.as_view(), name="classroom_delete"),
]
