from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from django.contrib import messages
from pay_ccavenue import CCAvenue
from django.conf import settings

from api.models import Sport, Team, Contact, Player, Payment
from .utils import listToString, stringToBool, initiatePayment, reduceArray
from .email_handler import send_registration_mail

from datetime import datetime
import shortuuid

class HomePageView(TemplateView):
    template_name = 'index.html'

class EventsPageView(View):

    def get(self, request, *args, **kwargs):
        introData = {
            'title': 'Events',
            'desc':'MIT-WPU Summit 2023 is back with 11 sports. Check them out below',
            'image':'/static/images/events.png',
            }
        # Exclude additional categories of swimming
        allSport = Sport.objects.exclude(logo='')
        for sport in allSport:
            sport.rules = sport.rules.split(';')
            n = len(sport.rules) if len(sport.rules) < 4 else 4
            sport.rules = reduceArray(sport.rules, n)
        context = {
                'introData': introData,
                'allSport': allSport,            }
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

class ConferencePageView(View):
    def get(self, request, *args, **kwargs):
        introData = {
            'title': 'Sports Conference',
            'desc':'',
            'image':'/static/images/events.png',
            }
        context = {
                'introData': introData
            }
        return render(request, 'conference.html',context)

class GuestsPageView(View):
     def get(self, request, *args, **kwargs):
        introData = {
            'title': 'Guests',
            'desc':'',
            'image':'/static/images/guests.png',
        }
        context = {
                'introData': introData
            }
        return render(request, 'guests.html',context)

class PrizesPageView(View):

    def get(self, request, *args, **kwargs):
        introData = {
            'title': 'Prizes',
            'desc':'',
            'image':'/static/images/prizes.png',
            }
        allSport = Sport.objects.exclude(logo="")
        for sport in allSport:
            sport.rules = sport.rules.split(';')
            n = len(sport.rules) if len(sport.rules) < 4 else 4
            sport.rules = reduceArray(sport.rules, n)
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
            'image':'/static/images/contact-us.png',
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
            relatedSports = Sport.objects.exclude(slug=sportSlug).exclude(logo='')
            introData = {
            'title': sportObject.name,
            'desc':'MIT-WPU Summit 2023 is back with 11 sports. Check them out below',
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
        amount = 0
        if gender == "all":
            gender = "men"
        # if sport == "":
            # Return 404 page
        # try:
        sportObject = Sport.objects.get(slug=sportSlug)
        introData = {
        'title': sportObject.name,
        'desc':'MIT-WPU Summit 2023 is back with 11 sports. Check them out below',
        'image':'/static/images/Banner_Homepage.svg',
        }

        # excluding captain
        if gender == 'men':
            miniList = [*range(1, sportObject.minimumPlayersMale, 1)]
            maxiList = [*range(sportObject.minimumPlayersMale, sportObject.maximumPlayersMale, 1)]
            amount = sportObject.priceMale
        elif gender == 'women':
            miniList = [*range(1, sportObject.minimumPlayersFemale, 1)]
            maxiList = [*range(sportObject.minimumPlayersFemale, sportObject.maximumPlayersFemale, 1)]
            amount = sportObject.priceFemale

        sportObject.minimumPlayers = miniList
        sportObject.maximumPlayers = maxiList
        context = {
            'sport': sportObject,
            'introData': introData,
            'amount': amount,
        }
        return render(request, 'sport_register.html', context)

        # except Exception as e:
        #     print(e)
            # Return 404 page

    def post(self, request, *args, **kwargs):

        params = self.kwargs['pk'].split('_')
        sportSlug = params[0]
        gender = params[1]
        if gender == "all":
            gender = "men"

        name = request.POST.get('fullname')
        email = request.POST.get('email')
        phone = request.POST.get('phone_number')
        state = request.POST.get('state')
        
        # Team details
        sport = Sport.objects.get(slug=sportSlug)
        college_name = request.POST.get('college_name')  
        institution_name = college_name if college_name != "" else request.POST.get('school_name')
        institution_type = request.POST.get('institution_type')
        need_accomodation = request.POST.get('accomodation')
        need_transport = request.POST.get('accomodation')
        need_meal = request.POST.get('need_meal')
        accomodation_preference = request.POST.get('accomodation_choice')
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

        order_id = datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(shortuuid.uuid())
        team = Team.objects.create(
            order_id = order_id,
            name = college_name,
            sport = sport,
            institute_name = college_name,
            institution_type = institution_type,
            need_accomodation = stringToBool(need_accomodation),
            need_transport = stringToBool(need_transport),
            need_meal = stringToBool(need_meal),
            accomodation_preference = accomodation_preference,
            sport_incharge_name = sports_incharge_name,
            sport_incharge_number = sports_incharge_number,
            sport_incharge_email_id = sports_incharge_email,
            player_names = listToString(player_names),
            captain_name = name,
            is_male_team = True if (gender == 'men' or gender == 'all' or gender == '') else False
        )

        for i in range(len(player_emails)):
            player = Player.objects.get_or_create(
                email = player_emails[i],
            )[0]
            
            player.name = player_names[i]
            player.phone = player_phones[i]
            player.team.add(team)
            player.state = state
            player.save()

        # Send request to payment gateway
        payment_context = initiatePayment(player_emails, team)
        
        return render(request, 'redirectPage.html', context=payment_context)

class UpdateTeamPage(View):
    def get(self, request, *args, **kwargs):
        
        transaction_id = self.kwargs['pk']
        payment = Payment.objects.get(tracking_id=int(transaction_id))
        team = Team.objects.get(payment=payment)
        players = Player.objects.filter(team=team)
        names = []
        emails = []
        phones = []
        
        for player in players:
            names.append(player.name)
            emails.append(player.email)
            phones.append(player.phone)

        introData = {
        'title': "Update Team Details",
        'image':'/static/images/Banner_Homepage.svg',
        }
        sportObject = team.sport
        miniList = [*range(1, sportObject.minimumPlayersMale+1, 1)]
        maxiList = [*range(sportObject.minimumPlayersMale+1, sportObject.maximumPlayersMale+1, 1)]
        sportObject.minimumPlayers = miniList
        sportObject.maximumPlayers = maxiList

        context = {
            "introData": introData,
            "sport": sportObject,
            "names": names,
            "emails": emails,
            "phones": phones,
            "team": team,
        }
        return render(request, 'update_team.html', context=context)

    def post(self, request, *args, **kwargs):

        transaction_id = self.kwargs['pk']
        payment = Payment.objects.get(tracking_id=int(transaction_id))
        team = Team.objects.get(payment=payment)

        if "Swimming" in team.sport.name and "Relay" not in team.sport.name:
            messages.info("You cannot edit swimming team details after payment. Please contact us for any queries.")
            return redirect('home')

        # Player details
        player_emails = [i for i in request.POST.getlist('player_emails') if i]
        player_phones = [i for i in request.POST.getlist('player_phones') if i]
        player_names = [i for i in request.POST.getlist('player_names') if i]

        # update team
        team.player_names = listToString(player_names)
        team.save()

        for i in range(len(player_names)):
            player = Player.objects.get_or_create(
                email = player_emails[i],
            )[0]
            
            player.name = player_names[i]
            player.phone = player_phones[i]
            player.team.add(team)
            player.save()
        
        if team.is_payment_successful:
            messages.info(request, 'Your team has been successfully edited!')
            return redirect('home')
        else:
            payment_context = initiatePayment(player_emails, team)
            return render(request, 'redirectPage.html', context=payment_context)