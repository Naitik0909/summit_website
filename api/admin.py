from django.contrib import admin
from csvexport.actions import csvexport

from .models import Sport, Contact, Team, Player, Payment

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
    list_display = ("name", "phone","message", "created_at", "is_resolved", "remarks")
    list_filter = ("is_resolved", )
    search_fields = ("name", "email", "phone")
    actions = [csvexport]

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "payment", "sport", "datetime", "captain_name", "player_names", "sport_incharge_name", "sport_incharge_number", "sport_incharge_email_id", "need_transport")
    search_fields = ("name", "institute_name", "captain_name", "sport_incharge_name", "sport_incharge_number", "sport_incharge_email_id", "order_id")
    list_filter = ("sport", "is_payment_successful", "is_male_team", "need_accomodation", "need_transport", "institution_type")
    actions = [csvexport]

    def changelist_view(self, request, extra_context=None):
        if not request.GET: #No filter
            temp = request.GET.copy()
            temp["is_payment_successful__exact"] = "1" #Set default filter
            request.GET = temp
        return super(TeamAdmin,self).changelist_view(request, extra_context=extra_context)


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone")
    list_filter = (PlayerSportsListFilter, TeamPlayersListFilter) 
    search_fields = ("name", "email", "phone", "team__name")
    actions = [csvexport]

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("tracking_id", "trans_date", "amount", "bank_ref_no", "order_status", "failure_message", "payment_mode", "card_name", "status_code", "status_message", "amount", "billing_name", "billing_address", "billing_city", "billing_state", "billing_zipcode", "billing_telephone", "billing_email")
    search_fields = ("amount", "bank_ref_no",)
    list_filter = ("order_status", "payment_mode", "billing_state", "billing_city")
    actions = [csvexport]