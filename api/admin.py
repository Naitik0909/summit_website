from django.contrib import admin
from .models import Sport, Contact, Team, Player

class TeamPlayersListFilter(admin.SimpleListFilter):
    title = 'Team'
    parameter_name = 'filter-by-team'

    def lookups(self, request, model_admin):
        teams = Team.objects.all()
        team_list = []
        for team in teams:
            team_list.append((team.id, f"{team.name} - {team.sport.name}"))
        return team_list

    def queryset(self, request, queryset):

        team_id = self.value()
        if team_id is not None:
            team = Team.objects.get(id=team_id)
            return queryset.filter(team=team)

@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):
    list_display = ("name", "venue", "price", "datetime", "minimumPlayers", "maximumPlayers")
    list_filter = ("venue", "price", "datetime", "minimumPlayers", "maximumPlayers")

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone","message")

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "institute_name", "sport", "datetime", "captain_name", "player_names", "sport_incharge_name", "sport_incharge_number", "sport_incharge_email_id")

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone")
    list_filter = (TeamPlayersListFilter, )
