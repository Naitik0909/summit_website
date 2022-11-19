from django.shortcuts import render
from django.views.generic import TemplateView, View

from api.models import Sport
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

class SportDetailPageView(View):

    def get(self, request, *args, **kwargs):
        sportSlug = self.kwargs['pk']
        # if sport == "":
            # Return 404 page
        try:
            sportObject = Sport.objects.get(slug=sportSlug)
            relatedSports = Sport.objects.exclude(slug=sportSlug).values('name', 'slug')
            print(relatedSports)
            context = {
                'sport': sportObject,
                'rules' : sportObject.rules.split(';'),
                'relatedSports' : relatedSports
            }
            return render(request, 'sport_detail.html', context)

        except Exception as e:
            print(e)
            # Return 404 page
