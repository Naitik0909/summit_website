from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View

from api.models import Sport, Team, Contact, Player
from .utils import listToString, stringToBool
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
            'desc':'',
            'image':'/static/images/Banner_Homepage.svg',
            }
        allSport = Sport.objects.all()
        for sport in allSport:
            sport.rules = sport.rules.split(';')
            n = len(sport.rules) if len(sport.rules) < 4 else 4
            sport.rules = PrizesPageView.reducaeArray(sport.rules, n)
        context = {
                'introData': introData,
                'allSport': allSport            }
        return render(request, 'events.html',context)

class AboutUsView(View):
    def get(self, request, *args, **kwargs):
        introData = {
            'title': 'About Us',
            'desc':'',
            'image':'/static/images/Banner_Homepage.svg',
            }
        context = {
                'introData': introData
            }
        return render(request, 'about.html',context)

class GuestsPageView(View):
     def get(self, request, *args, **kwargs):
        introData = {
            'title': 'Guests',
            'desc':'',
            'image':'/static/images/Banner_Homepage.svg',
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
            'desc':'',
            'image':'/static/images/Banner_Homepage.svg',
            }
        allSport = Sport.objects.all()
        for sport in allSport:
            sport.rules = sport.rules.split(';')
            n = len(sport.rules) if len(sport.rules) < 4 else 4
            sport.rules = PrizesPageView.reducaeArray(sport.rules, n)
        context = {
                'introData': introData,
                'allSport': allSport            }
        return render(request, 'prizes.html',context)

class GalleryPageView(View):
     def get(self, request, *args, **kwargs):
        introData = {
            'title': 'Gallery',
            'desc':'',
            'image':'/static/images/Banner_Homepage.svg',
           
        }
        context = {
                'introData': introData
            }
        return render(request, 'gallery.html',context)



class TeamAndContactPageView(View):
    def get(self, request, *args, **kwargs):
        introData = {
            'title': 'Contact Us',
            'desc':'',
            'image':'/static/images/Banner_Homepage.svg',
            # 'question':'What are you looking for?',
            # 'information':'ipsum dolor sit amet, consectetur adipisicing elit. Ea dolorem sequi, quo tempore in eum obcaecati atque quibusdam officiis est dolorum minima deleniti ratione molestias numquam. Voluptas voluptates quibusdam cum?'
       
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
            'image':'/static/images/Banner_Homepage.svg',

            # 'desc':'ipsum dolor sit amet, consectetur adipisicing elit. Ea dolorem sequi, quo tempore in eum obcaecati atque quibusdam officiis est dolorum minima deleniti ratione molestias numquam. Voluptas voluptates quibusdam cum?',
            # 'question':'What are you looking for?',
            # 'information':'ipsum dolor sit amet, consectetur adipisicing elit. Ea dolorem sequi, quo tempore in eum obcaecati atque quibusdam officiis est dolorum minima deleniti ratione molestias numquam. Voluptas voluptates quibusdam cum?'
       
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
            relatedSports = Sport.objects.exclude(slug=sportSlug)
            introData = {
            'title': sportObject.name,
            'desc':sportObject.description,
            'image':sportObject.image.url,
            }   
            context = {
                'sport': sportObject,
                'relatedSports' : relatedSports,
                'introData': introData
                
            }
            return render(request, 'sport_detail.html', context)

        except Exception as e:
            print(e)
            # Return 404 page

class SportRegisterPageView(View):

    def get(self, request, *args, **kwargs):
        params = self.kwargs['pk'].split('_')
        sportSlug = params[0]
        gender = params[1]
        # if sport == "":
            # Return 404 page
        try:
            sportObject = Sport.objects.get(slug=sportSlug)
            introData = {
            'title': sportObject.name,
            'desc':sportObject.description,
            'image':'/static/images/Banner_Homepage.svg',
            }
            if gender == 'men':
                miniList = [*range(1, sportObject.minimumPlayersMale+1, 1)]
                maxiList = [*range(sportObject.minimumPlayersMale+1, sportObject.maximumPlayersMale+1, 1)]
            elif gender == 'women':
                miniList = [*range(1, sportObject.minimumPlayersFemale+1, 1)]
                maxiList = [*range(sportObject.minimumPlayersFemale+1, sportObject.maximumPlayersFemale+1, 1)]
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

        sportSlug = self.kwargs['pk']
        name = request.POST.get('fullname')
        email = request.POST.get('email')
        phone = request.POST.get('phone_number')
        state = request.POST.get('state')
        
        # Team details
        sport = Sport.objects.get(slug=sportSlug)
        college_name = request.POST.get('college_name')  
        institution_name = college_name if college_name != "" else request.POST.get('school_name')
        need_accomodation = request.POST.get('accomodation')
        sports_incharge_name = request.POST.get('sportsincharge_name')
        sports_incharge_number = request.POST.get('sportsincharge_number')
        sports_incharge_email = request.POST.get('sportsincharge_email')
        
        # Player details
        player_names = request.POST.getlist('player_names')
        player_emails = request.POST.getlist('player_emails')
        player_phones = request.POST.getlist('player_phones')

        player_emails.append(email)
        player_phones.append(phone)
        player_names.append(name)

        player_emails = [i for i in player_emails if i]
        player_phones = [i for i in player_phones if i]
        player_names = [i for i in player_names if i]
        print(player_names)
        
        team = Team.objects.create(
            name = college_name,
            sport = sport,
            institute_name = college_name,
            need_accomodation = stringToBool(need_accomodation),
            sport_incharge_name = sports_incharge_name,
            sport_incharge_number = sports_incharge_number,
            sport_incharge_email_id = sports_incharge_email,
            player_names = listToString(player_names),
            captain_name = name
        )

        for i in range(len(player_names)):
            player = Player.objects.get_or_create(
                email = player_emails[i],
            )[0]
            
            player.name = player_names[i]
            player.phone = player_phones[i]
            player.team.add(team)
            player.save()


        return redirect('home')

class PartialForm(View):


    def get(self, request, *args, **kwargs):
        introData = {
                'title': "Update Form Details",
                'image':'/static/images/Banner_Homepage.svg',
                }
        context = {
            "introData": introData
        }
        return render(request, 'partial_form.html', context=context)