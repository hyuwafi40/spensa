from django.db import models
from core.models.account import CustomUser
from core.models.base import TimeStampedMixin
from core.utils.constants import JournalActivityChoices, LogLevelChoices


class DeveloperLog(TimeStampedMixin):
    level = models.CharField(
        max_length=20, choices=LogLevelChoices.choices, default=LogLevelChoices.INFO
    )
    event = models.CharField(max_length=255)
    path = models.CharField(max_length=255, blank=True)
    method = models.CharField(max_length=10, blank=True)
    status_code = models.PositiveSmallIntegerField(null=True, blank=True)
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="developer_logs",
    )
    module = models.CharField(max_length=50, blank=True)
    object_id = models.PositiveBigIntegerField(null=True, blank=True)
    action = models.CharField(
        max_length=20, choices=JournalActivityChoices.choices, blank=True
    )
    object_repr = models.CharField(max_length=255, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        verbose_name = "Log Developer"
        verbose_name_plural = "Log Developer"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["level"]),
            models.Index(fields=["status_code"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["module", "action"]),
        ]

    def __str__(self):
        return f"[{self.level}] {self.event} - {self.path}"
