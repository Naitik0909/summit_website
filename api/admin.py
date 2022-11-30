from django.contrib import admin
from .models import Sport, Contact, Team, Player

@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):
    list_display = ("name", "venue", "price", "datetime", "minimumPlayers", "maximumPlayers")
    list_filter = ("venue", "price", "datetime", "minimumPlayers", "maximumPlayers")

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone","message")

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "team_type", "institute_name", "sport", "datetime", "sport_incharge_name", "sport_incharge_number", "sport_incharge_email_id")

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "college_id", "aadhar_card_number")
