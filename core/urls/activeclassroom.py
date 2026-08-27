from django.urls import path
from core.views.activeclassroom import (
    ActiveClassroomListView,
    ActiveClassroomCreateView,
    ActiveClassroomUpdateView,
    ActiveClassroomDeleteView,
    ActiveStudentListView,
    ActiveStudentCreateView,
    ActiveStudentUpdateView,
    ActiveStudentDeleteView,
)

urlpatterns = [
    path("active-classrooms/", ActiveClassroomListView.as_view(), name="active_classroom"),
    path("active-classrooms/create/", ActiveClassroomCreateView.as_view(), name="active_classroom_create"),
    path("active-classrooms/<int:pk>/update/", ActiveClassroomUpdateView.as_view(), name="active_classroom_update"),
    path("active-classrooms/<int:pk>/delete/", ActiveClassroomDeleteView.as_view(), name="active_classroom_delete"),
    path("active-classrooms/<int:classroom_id>/students/", ActiveStudentListView.as_view(), name="active_student_list"),
    path("active-classrooms/<int:classroom_id>/students/create/", ActiveStudentCreateView.as_view(), name="active_student_create"),
    path("active-classrooms/students/<int:pk>/update/", ActiveStudentUpdateView.as_view(), name="active_student_update"),
    path("active-classrooms/students/<int:pk>/delete/", ActiveStudentDeleteView.as_view(), name="active_student_delete"),
]
