from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Action(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=["-created"]),
            models.Index(fields=["target_content_type", "target_id"]),
        ]
        ordering = ["-created"]
    user = models.ForeignKey("auth.User", related_name="actions", on_delete=models.CASCADE)
    verb = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)
    target_content_type = models.ForeignKey(ContentType, blank=True, null=True, on_delete=models.CASCADE, related_name="target_obj")
    target_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey("target_content_type", "target_id")