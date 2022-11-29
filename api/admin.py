from django.contrib import admin
from .models import Sport,Contact

@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):
    list_display = ("name", "venue", "price", "datetime", "minimumPlayers", "maximumPlayers")
    list_filter = ("venue", "price", "datetime", "minimumPlayers", "maximumPlayers")

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone","message")
