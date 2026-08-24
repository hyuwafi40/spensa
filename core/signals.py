from django.apps import apps
from django.db.models.signals import post_save
from django.dispatch import receiver
from core.utils.services import sync_username_from_profile


@receiver(post_save, sender=apps.get_model("core", "Profile"))
def sync_username(sender, instance, **kwargs):
    sync_username_from_profile(instance)
