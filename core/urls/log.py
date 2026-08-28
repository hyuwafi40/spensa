from django.urls import path
from core.views.log import LogListView

urlpatterns = [
    path("logs/", LogListView.as_view(), name="log_activity"),
]
