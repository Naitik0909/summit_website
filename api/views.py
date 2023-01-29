from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from pay_ccavenue import CCAvenue

from api.models import Payment, Team, Player
from frontend.email_handler import send_registration_mail

from datetime import datetime
import shortuuid
from string import Template

@method_decorator(csrf_exempt, name='dispatch')
class PaymentForm(TemplateView):
    template_name = 'dataFrom.html'

@method_decorator(csrf_exempt, name='dispatch')
class CCAveReqeustHandler(View):

    def post(self, request, *args, **kwargs):

        reqObj = {
            'merchant_id': settings.CC_AVENUE_MERCHANT_ID,
            'order_id': datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(shortuuid.uuid()),
            'currency': settings.CC_AVENUE_CURRENCY,
            'redirect_url':settings.CC_AVENUE_SUCCESS_URL,
            'cancel_url': settings.CC_AVENUE_FAILURE_URL,
            'language': settings.CC_AVENUE_LANG,
            'amount': 1,
        }
        ccavenue = CCAvenue()
        encrypt_data = ccavenue.encrypt(reqObj)
        context = {
            "encReq": encrypt_data,
            "xscode": settings.CC_AVENUE_ACCESS_CODE,
            "ccAveURL": settings.CC_AVENUE_URL,
        }
        return render(request, 'redirectPage.html', context=context)


@method_decorator(csrf_exempt, name='dispatch')
class CCAveResposeHandler(View):

    def post(self, request, *args, **kwargs):
        try:
            encResp = request.POST.get('encResp')

            reqObj = {
                'encResp' : encResp 
            }
            ccavenue = CCAvenue()
            decResp = ccavenue.decrypt(reqObj)
            order_id = decResp["order_id"]

            format = '%d/%m/%Y %H:%M:%S'
            failed = False
            payment = Payment.objects.create(
                tracking_id = decResp["tracking_id"],
                amount = decResp["amount"],
                bank_ref_no = decResp["bank_ref_no"],
                order_status = decResp["order_status"],
                failure_message = decResp["failure_message"],
                payment_mode = decResp["payment_mode"],
                card_name = decResp["card_name"],
                status_code = decResp["status_code"],
                status_message = decResp["status_message"],
                trans_date = datetime.strptime(decResp["trans_date"], format),
                billing_name = decResp["billing_name"],
                billing_address = decResp["billing_address"],
                billing_city = decResp["billing_city"],
                billing_state = decResp["billing_state"],
                billing_zipcode = decResp["billing_zip"],
                billing_telephone = decResp["billing_tel"],
                billing_email = decResp["billing_email"],
            )

            team = Team.objects.get(order_id=order_id)
            team.payment = payment

            if(decResp["order_status"] == "Success"):
                team.is_payment_successful = True
                try:
                    team_update_url = request.build_absolute_uri("/update_team/" + str(decResp["tracking_id"]))
                    logo_url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/media/{team.sport.logo}"
                    send_registration_mail(decResp["billing_email"], logo_url, team_update_url)
                except Exception as e:
                    print("---------Email Exception---------", e)
                team.save()
            else:
                failed = True
                team.is_payment_successful = False
                team.save()

            decResp["failed"] = failed
            context = {
                "response": decResp
            }
        
        except Exception as e:
            print("---------Exception---------", e)
            messages.warning(request, "Something went wrong. Please try again later.")
            return redirect('home')
        return render(request, "response1.html", context=context)

@csrf_exempt
def validateSwimming(request):
    if request.method == "POST":
        response = []
        player_emails = request.POST.getlist('emails[]')
        print(request.POST)
        for email in player_emails:
            try:
                player = Player.objects.get(email=email)
            except ObjectDoesNotExist:
                response.append(True)
                continue
                
            registration_count = 0
            for team in player.team.all():
                if "Swimming" in team.sport.name and "Relay" not in team.sport.name:
                    registration_count+=1
            if registration_count >= 2:
                response.append(False)
            else:
                response.append(True)
        return JsonResponse(response, safe=False)
    else:
        return redirect('home')