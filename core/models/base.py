from django.db import models
from core.utils.services import generate_unique_slug


class TimeStampedMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SlugMixin(models.Model):
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(
                self.__class__, self.get_slug_source(), instance=self
            )
        super().save(*args, **kwargs)

    def get_slug_source(self):
        raise NotImplementedError("Subclass must implement get_slug_source()")
