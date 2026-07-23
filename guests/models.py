from django.db import models

from wedding.models import Wedding


class Guest(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pendente"
        CONFIRMED = "CONFIRMED", "Confirmado"
        DECLINED = "DECLINED", "Recusado"

    wedding = models.ForeignKey(
        Wedding,
        on_delete=models.CASCADE,
        related_name="guests",
    )

    full_name = models.CharField(
        max_length=255,
    )

    email = models.EmailField()

    phone = models.CharField(
        max_length=20,
        blank=True,
    )

    invitation_code = models.CharField(
        max_length=50,
        unique=True,
    )

    companions = models.PositiveIntegerField(
        default=0,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    notes = models.TextField(
        blank=True,
    )

    # RSVP
    confirmed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    message = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["full_name"]

    def __str__(self):
        return self.full_name
