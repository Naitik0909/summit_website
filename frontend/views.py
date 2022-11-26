from django.shortcuts import render
from django.views.generic import TemplateView, View

from api.models import Sport
class HomePageView(TemplateView):
    template_name = 'index.html'

class EventsPageView(View):
    # Custom function to reduce rules
    def reducaeArray(arr,n):
        newArr = []
        for i in range(0,n):
            newArr.append(arr[i])
        return newArr

    def get(self, request, *args, **kwargs):
        print(request.resolver_match.view_name)
        introData = {
            'title': 'Events',
            'desc':'Lorem ipsum dummy text',
            'image':'/static/images/Banner_Homepage.svg',
            }
        allSport = Sport.objects.all()
        for sport in allSport:
            sport.rules = sport.rules.split(';');
            sport.rules = EventsPageView.reducaeArray(sport.rules, 4)
        context = {
                'introData': introData,
                'allSport': allSport            }
        return render(request, 'events.html',context)

class GuestsPageView(View):
     def get(self, request, *args, **kwargs):
        introData = {
            'title': 'Guests',
            'desc':'Lorem ipsum dummy text',
            
       
        }
        context = {
                'introData': introData
            }
        return render(request, 'guests.html',context)

class PrizesPageView(View):

    def reducaeArray(arr,n):
        newArr = []
        for i in range(0,n):
            newArr.append(arr[i])
        return newArr

    def get(self, request, *args, **kwargs):
        print(request.resolver_match.view_name)
        introData = {
            'title': 'Prizes',
            'desc':'Lorem ipsum dummy text',
            }
        allSport = Sport.objects.all()
        for sport in allSport:
            sport.rules = sport.rules.split(';');
            sport.rules = PrizesPageView.reducaeArray(sport.rules, 4)
        context = {
                'introData': introData,
                'allSport': allSport            }
        return render(request, 'prizes.html',context)

class GalleryPageView(View):
     def get(self, request, *args, **kwargs):
        introData = {
            'title': 'Gallery',
            'desc':'Lorem ipsum dummy text',
           
        }
        context = {
                'introData': introData
            }
        return render(request, 'gallery.html',context)



class TeamAndContactPageView(View):
    def get(self, request, *args, **kwargs):
        introData = {
            'title': 'Contact Us',
            'desc':'ipsum dolor sit amet, consectetur adipisicing elit. Ea dolorem sequi, quo tempore in eum obcaecati atque quibusdam officiis est dolorum minima deleniti ratione molestias numquam. Voluptas voluptates quibusdam cum?',
            # 'question':'What are you looking for?',
            'information':'ipsum dolor sit amet, consectetur adipisicing elit. Ea dolorem sequi, quo tempore in eum obcaecati atque quibusdam officiis est dolorum minima deleniti ratione molestias numquam. Voluptas voluptates quibusdam cum?'
       
        }
        context = {
                'introData': introData
            }
        return render(request, 'team_and_contact.html',context)

class ScoresAndFixturesPageView(View):
    def get(self, request, *args, **kwargs):

        introData = {
            'title': 'Scores & Fixtures',
            'desc':'ipsum dolor sit amet, consectetur adipisicing elit. Ea dolorem sequi, quo tempore in eum obcaecati atque quibusdam officiis est dolorum minima deleniti ratione molestias numquam. Voluptas voluptates quibusdam cum?',
            'question':'What are you looking for?',
            'information':'ipsum dolor sit amet, consectetur adipisicing elit. Ea dolorem sequi, quo tempore in eum obcaecati atque quibusdam officiis est dolorum minima deleniti ratione molestias numquam. Voluptas voluptates quibusdam cum?'
       
        }
        context = {
                'introData': introData
            }
        return render(request, 'scores_and_fixtures.html',context)

class SportDetailPageView(View):

    def get(self, request, *args, **kwargs):
        sportSlug = self.kwargs['pk']
        # if sport == "":
            # Return 404 page
        try:
            sportObject = Sport.objects.get(slug=sportSlug)
            relatedSports = Sport.objects.exclude(slug=sportSlug).values('name', 'slug')
            print(relatedSports)
            introData = {
            'title': sportObject.name,
            'desc':sportObject.description,
            'image':sportObject.image.url,
            }   
            context = {
                'sport': sportObject,
                'rules' : sportObject.rules.split(';'),
                'relatedSports' : relatedSports,
                'introData': introData
                
            }
            return render(request, 'sport_detail.html', context)

        except Exception as e:
            print(e)
            # Return 404 page

class SportRegisterPageView(View):

    def get(self, request, *args, **kwargs):
        sportSlug = self.kwargs['pk']
        # if sport == "":
            # Return 404 page
        try:
            sportObject = Sport.objects.get(slug=sportSlug)
            introData = {
            'title': sportObject.name,
            'desc':sportObject.description,
            }   
            miniList = [*range(1, sportObject.minimumPlayers+1, 1)]
            maxiList = [*range(sportObject.minimumPlayers+1, sportObject.maximumPlayers+1, 1)]
            sportObject.minimumPlayers = miniList
            sportObject.maximumPlayers = maxiList
            context = {
                'sport': sportObject,
                'introData': introData
            }
            print(sportObject.minimumPlayers)
            return render(request, 'sport_register.html', context)

        except Exception as e:
            print(e)
            # Return 404 page
