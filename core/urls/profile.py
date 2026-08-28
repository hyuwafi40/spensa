from django.urls import path
from core.views.profile import ProfilePageView, ProfileUpdateView

urlpatterns = [
    path("profile/", ProfilePageView.as_view(), name="profile"),
    path("profile/update/", ProfileUpdateView.as_view(), name="profile_update"),
]
