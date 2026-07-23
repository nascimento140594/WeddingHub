from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Wedding(models.Model):
    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="wedding",
    )

    title = models.CharField(
        max_length=150,
        default="Meu Casamento",
    )

    slug = models.SlugField(
        unique=True,
        max_length=150,
        blank=True,
    )

    bride_name = models.CharField(
        max_length=100,
    )

    groom_name = models.CharField(
        max_length=100,
    )

    wedding_date = models.DateField()

    ceremony_time = models.TimeField(
        default="16:00:00",
    )

    ceremony_address = models.CharField(
        max_length=255,
    )

    reception_address = models.CharField(
        max_length=255,
        blank=True,
        default="",
    )

    city = models.CharField(
        max_length=100,
    )

    state = models.CharField(
        max_length=2,
    )

    about = models.TextField(
        blank=True,
    )

    cover_image = models.ImageField(
        upload_to="weddings/covers/",
        blank=True,
        null=True,
    )

    primary_color = models.CharField(
        max_length=7,
        default="#C8A97E",
    )

    secondary_color = models.CharField(
        max_length=7,
        default="#FFFFFF",
    )

    instagram_hashtag = models.CharField(
        max_length=100,
        blank=True,
        default="",
    )

    pix_key = models.CharField(
        max_length=255,
        blank=True,
        default="",
    )

    is_public = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["wedding_date"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
