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
from .utils import getFormatedDate

from datetime import datetime
import shortuuid
from string import Template
import pytz

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
            tz = pytz.timezone("Asia/Kolkata") 
            time = datetime.now(tz)
            currTime = time.strftime("%d-%m-%Y - %H:%M:%S")
            encResp = request.POST.get('encResp')
            print(currTime+"--------------New Payment Respose-------------", encResp)

            reqObj = {
                'encResp' : encResp 
            }
            ccavenue = CCAvenue()
            decResp = ccavenue.decrypt(reqObj)
            print(currTime+"--------------Decrypted data-------------", decResp)
            order_id = decResp.get("order_id", "")

            failed = False
            payment = Payment.objects.create(
                tracking_id = decResp.get("tracking_id", ""),
                amount = decResp.get("amount", ""),
                bank_ref_no = decResp.get("bank_ref_no", ""),
                order_status = decResp.get("order_status", ""),
                failure_message = decResp.get("failure_message", ""),
                payment_mode = decResp.get("payment_mode", ""),
                card_name = decResp.get("card_name", ""),
                status_code = decResp.get("status_code", ""),
                status_message = decResp.get("status_message", ""),
                trans_date = getFormatedDate(decResp.get("trans_date", "")),
                billing_name = decResp.get("billing_name", ""),
                billing_address = decResp.get("billing_address", ""),
                billing_city = decResp.get("billing_city", ""),
                billing_state = decResp.get("billing_state", ""),
                billing_zipcode = decResp.get("billing_zip", ""),
                billing_telephone = decResp.get("billing_tel", ""),
                billing_email = decResp.get("billing_email", ""),
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
            tz = pytz.timezone("Asia/Kolkata") 
            time = datetime.now(tz)
            currTime = time.strftime("%d-%m-%Y - %H:%M:%S")
            # Append-adds at last
            file1 = open("summit_err_log.txt", "a")  # append mode
            file1.write(currTime+"---------Exception in payments--------- "+str(e))
            file1.close()
            print(currTime+"---------Exception in payments---------", str(e))
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