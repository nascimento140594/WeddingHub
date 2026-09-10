import secrets

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
        blank=True,
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

    def save(self, *args, **kwargs):

        if not self.invitation_code:

            while True:

                code = secrets.token_urlsafe(8)

                if not Guest.objects.filter(
                    invitation_code=code,
                ).exists():

                    self.invitation_code = code

                    break

        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name
