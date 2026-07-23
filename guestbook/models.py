from django.db import models

from wedding.models import Wedding


class GuestMessage(models.Model):
    wedding = models.ForeignKey(
        Wedding,
        on_delete=models.CASCADE,
        related_name="messages",
    )

    guest_name = models.CharField(
        max_length=255,
    )

    guest_email = models.EmailField(
        blank=True,
    )

    message = models.TextField()

    approved = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.guest_name
