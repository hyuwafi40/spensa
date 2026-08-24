from django.contrib.auth.models import UserManager
from core.utils.services import set_role_flags


class CustomUserManager(UserManager):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("job", "developer")
        user = self._create_user(username, email, password, **extra_fields)
        set_role_flags(user, user.job)
        user.save(update_fields=["is_active", "is_staff", "is_superuser"])
        return user
