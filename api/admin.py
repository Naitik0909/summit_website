from django.contrib import admin
from csvexport.actions import csvexport

from .models import Sport, Contact, Team, Player

class TeamPlayersListFilter(admin.SimpleListFilter):
    title = 'Team'
    parameter_name = 'team'

    def lookups(self, request, model_admin):
        team_list = []
        selected_sport = request.GET.get('sport', '')
        if selected_sport:
            sport = Sport.objects.get(id=selected_sport)
            teams = Team.objects.filter(sport=sport)
        else:
            teams = Team.objects.all()
        for team in teams:
            team_list.append((team.id, f"{team.name} - {team.sport.name}"))
        return team_list

    def queryset(self, request, queryset):

        team_id = self.value()
        if team_id is not None:
            team = Team.objects.get(id=team_id)
            return queryset.filter(team=team)

class PlayerSportsListFilter(admin.SimpleListFilter):
    title = 'Sport'
    parameter_name = 'sport'

    def lookups(self, request, model_admin):
        sports = Sport.objects.all()
        sport_list = []
        for sport in sports:
            sport_list.append((sport.id, f"{sport.name}"))
        return sport_list

    def queryset(self, request, queryset):

        sport_id = self.value()
        if sport_id is not None:
            sport = Sport.objects.get(id=sport_id)
            return queryset.filter(team__sport=sport).distinct()

@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):
    list_display = ("name", "venue", "priceMale","priceFemale", "datetime", "minimumPlayersMale", "maximumPlayersMale","minimumPlayersFemale","maximumPlayersFemale")
    list_filter = ("venue",  "priceMale","priceFemale", "datetime", "minimumPlayersMale", "maximumPlayersMale","minimumPlayersFemale","maximumPlayersFemale")
    search_fields = ("name",)
    actions = [csvexport]

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone","message")
    search_fields = ("name", "email", "phone")
    actions = [csvexport]

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "institute_name", "sport", "datetime", "captain_name", "player_names", "sport_incharge_name", "sport_incharge_number", "sport_incharge_email_id")
    search_fields = ("name", "institute_name", "captain_name", "sport_incharge_name", "sport_incharge_number", "sport_incharge_email_id")
    list_filter = ("sport", )
    actions = [csvexport]

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone")
    list_filter = (PlayerSportsListFilter, TeamPlayersListFilter) 
    search_fields = ("name", "email", "phone", "team__name")
    actions = [csvexport]
