from django.db import models


class Measurement(models.Model):
    device_id = models.CharField(
        max_length=10, help_text="A random device identifier")
    mode = models.CharField(
        max_length=56, help_text="Data collection mode (for selecting analysis)")
    measurement_data = models.JSONField(help_text="Measurement data in JSON")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.device_id}/{self.mode} ({self.id})"
