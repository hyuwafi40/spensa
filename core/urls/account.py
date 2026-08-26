from django.urls import path
from core.views.account import (
    AccountListView,
    AccountCreateView,
    AccountUpdateView,
    AccountDeleteView,
    AccountResetPasswordView,
)

urlpatterns = [
    path("accounts/", AccountListView.as_view(), name="user_account"),
    path("accounts/create/", AccountCreateView.as_view(), name="account_create"),
    path("accounts/<int:pk>/update/", AccountUpdateView.as_view(), name="account_update"),
    path("accounts/<int:pk>/delete/", AccountDeleteView.as_view(), name="account_delete"),
    path("accounts/<int:pk>/reset-password/", AccountResetPasswordView.as_view(), name="account_reset_password"),
]