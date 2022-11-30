from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View

from api.models import Sport, Team, Contact, Player
from .utils import listToString
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

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        query = Contact.objects.create(
            name = name,
            email = email,
            phone = phone,
            message = message
        )
        return redirect('home')

class ScoresAndFixturesPageView(View):
    def get(self, request, *args, **kwargs):

        introData = {
            'title': 'Scores & Fixtures',
            'desc':'ipsum dolor sit amet, consectetur adipisicing elit. Ea dolorem sequi, quo tempore in eum obcaecati atque quibusdam officiis est dolorum minima deleniti ratione molestias numquam. Voluptas voluptates quibusdam cum?',
            # 'question':'What are you looking for?',
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
            return render(request, 'sport_register.html', context)

        except Exception as e:
            print(e)
            # Return 404 page

    def post(self, request, *args, **kwargs):

        # sportSlug = self.kwargs['pk']
        # name = f"{request.POST.get('first_name')} {request.POST.get('last_name')}"
        # email = request.POST.get('email')
        # phone = request.POST.get('phone_number')
        # aadhar_number = request.POST.get('Aadhar_number')
        # state = request.POST.get('state')
        # try:
        #     college_id = request.FILES['college_id']
        # except Exception as e:
        #     print(e)
        
        # # Team details
        # sport = Sport.objects.get(slug=sportSlug)
        # college_name = request.POST.get('college_name')  
        # institution_name = college_name if college_name != "" else request.POST.get('school_name')
        # need_accomodation = request.POST.get('accomodation')
        # sports_incharge_name = request.POST.get('sportsincharge_name')
        # sports_incharge_number = request.POST.get('sportsincharge_number')
        # sports_incharge_email = request.POST.get('sportsincharge_email')
        # pool = request.POST.get('pool')
        
        # # Player details
        # player_names = request.POST.getlist('player_name')
        
        # team = Team.objects.create(
        #     sport = sport,
        #     institution_name = institution_name,
        #     need_accomodation = need_accomodation,
        #     sports_incharge_name = sports_incharge_name,
        #     sports_incharge_number = sports_incharge_number,
        #     sports_incharge_email = sports_incharge_email,
        #     pool = pool,
        #     player_names = listToString(player_names)
        # )

        # player = Player.objects.get_or_create(email=email)
        # player.


        return redirect('home')
