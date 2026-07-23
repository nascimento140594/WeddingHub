from django.db import models

from gifts.models import Gift


class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pendente"
        PAID = "PAID", "Pago"
        FAILED = "FAILED", "Falhou"
        REFUNDED = "REFUNDED", "Reembolsado"

    gift = models.ForeignKey(
        Gift,
        on_delete=models.CASCADE,
        related_name="payments",
    )

    guest_name = models.CharField(
        max_length=255,
    )

    guest_email = models.EmailField()

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    transaction_id = models.CharField(
        max_length=255,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.guest_name} - {self.amount}"
