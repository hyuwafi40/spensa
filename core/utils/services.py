import uuid
from django.db import transaction
from django.utils.text import slugify


def set_role_flags(user, job):
    flags = {
        "developer": {"is_active": True, "is_staff": True, "is_superuser": True},
        "administrator": {"is_active": True, "is_staff": True, "is_superuser": False},
        "teacher": {"is_active": True, "is_staff": False, "is_superuser": False},
        "student": {"is_active": True, "is_staff": False, "is_superuser": False},
    }
    flags = flags.get(job)
    if flags:
        user.is_active = flags["is_active"]
        user.is_staff = flags["is_staff"]
        user.is_superuser = flags["is_superuser"]


def generate_username():
    return uuid.uuid4().hex[:12]


def sync_username_from_profile(profile):
    if profile.code:
        if profile.user.username != profile.code:
            profile.user.username = profile.code
            profile.user.save(update_fields=["username"])


def generate_unique_slug(model, name, instance=None):
    base_slug = slugify(name)
    slug = base_slug
    counter = 1
    while True:
        query = model.objects.filter(slug=slug)
        if instance:
            query = query.exclude(pk=instance.pk)
        if not query.exists():
            return slug
        slug = f"{base_slug}-{counter}"
        counter += 1


def set_active_year(instance):
    with transaction.atomic():
        if instance.is_active:
            queryset = instance.__class__.objects.select_for_update()
            if instance.pk is not None:
                queryset = queryset.exclude(pk=instance.pk)
            queryset.update(is_active=False)
