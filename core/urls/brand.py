from django.urls import path
from core.views.brand import BrandPageView, BrandCreateView, BrandUpdateView

urlpatterns = [
    path("brand/", BrandPageView.as_view(), name="brand"),
    path("brand/create/", BrandCreateView.as_view(), name="brand_create"),
    path("brand/update/", BrandUpdateView.as_view(), name="brand_update"),
]
