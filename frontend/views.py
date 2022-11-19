from django.shortcuts import render
from django.views.generic import TemplateView, View

class HomePageView(TemplateView):
    template_name = 'index.html'

class EventsPageView(TemplateView):
    template_name = 'events.html'

class GuestsAndPricesPageView(TemplateView):
    template_name = 'guests_and_prices.html'

class TeamAndContactPageView(TemplateView):
    template_name = 'team_and_contact.html'

class ScoresAndFixturesPageView(TemplateView):
    template_name = 'scores_and_fixtures.html'
