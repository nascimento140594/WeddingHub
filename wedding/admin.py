from django.contrib import admin

from .models import Wedding


@admin.register(Wedding)
class WeddingAdmin(admin.ModelAdmin):
    list_display = (
        "bride_name",
        "groom_name",
        "wedding_date",
        "city",
        "state",
    )

    search_fields = (
        "bride_name",
        "groom_name",
        "city",
    )

    list_filter = (
        "state",
    )
