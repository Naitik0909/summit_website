from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View

from string import Template

from api.ccavutil import encrypt, decrypt


class PaymentForm(TemplateView):
    template_name = 'dataFrom.html'

class CCAveReqeustHandler(View):

    def post(self, request, *args, **kwargs):

        p_merchant_id = request.POST['merchant_id']
        p_order_id = request.POST['order_id']
        p_currency = request.POST['currency']
        p_amount = request.POST['amount']
        p_redirect_url = request.POST['redirect_url']
        p_cancel_url = request.POST['cancel_url']
        p_language = request.POST['language']
        p_billing_name = request.POST['billing_name']
        p_billing_address = request.POST['billing_address']
        p_billing_city = request.POST['billing_city']
        p_billing_state = request.POST['billing_state']
        p_billing_zip = request.POST['billing_zip']
        p_billing_country = request.POST['billing_country']
        p_billing_tel = request.POST['billing_tel']
        p_billing_email = request.POST['billing_email']
        p_delivery_name = request.POST['delivery_name']
        p_delivery_address = request.POST['delivery_address']
        p_delivery_city = request.POST['delivery_city']
        p_delivery_state = request.POST['delivery_state']
        p_delivery_zip = request.POST['delivery_zip']
        p_delivery_country = request.POST['delivery_country']
        p_delivery_tel = request.POST['delivery_tel']
        p_merchant_param1 = request.POST['merchant_param1']
        p_merchant_param2 = request.POST['merchant_param2']
        p_merchant_param3 = request.POST['merchant_param3']
        p_merchant_param4 = request.POST['merchant_param4']
        p_merchant_param5 = request.POST['merchant_param5']
        p_promo_code = request.POST['promo_code']
        p_customer_identifier = request.POST['customer_identifier']

        merchant_data='merchant_id='+p_merchant_id+'&'+'order_id='+p_order_id + '&' + "currency=" + p_currency + '&' + 'amount=' + p_amount+'&'+'redirect_url='+p_redirect_url+'&'+'cancel_url='+p_cancel_url+'&'+'language='+p_language+'&'+'billing_name='+p_billing_name+'&'+'billing_address='+p_billing_address+'&'+'billing_city='+p_billing_city+'&'+'billing_state='+p_billing_state+'&'+'billing_zip='+p_billing_zip+'&'+'billing_country='+p_billing_country+'&'+'billing_tel='+p_billing_tel+'&'+'billing_email='+p_billing_email+'&'+'delivery_name='+p_delivery_name+'&'+'delivery_address='+p_delivery_address+'&'+'delivery_city='+p_delivery_city+'&'+'delivery_state='+p_delivery_state+'&'+'delivery_zip='+p_delivery_zip+'&'+'delivery_country='+p_delivery_country+'&'+'delivery_tel='+p_delivery_tel+'&'+'merchant_param1='+p_merchant_param1+'&'+'merchant_param2='+p_merchant_param2+'&'+'merchant_param3='+p_merchant_param3+'&'+'merchant_param4='+p_merchant_param4+'&'+'merchant_param5='+p_merchant_param5+'&'+'promo_code='+p_promo_code+'&'+'customer_identifier='+p_customer_identifier+'&'
            
        encryption = encrypt(merchant_data,workingKey)

        html = '''\
            <html>
            <head>
                <title>Sub-merchant checkout page</title>
                <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
            </head>
            <body>
            <form id="nonseamless" method="post" name="redirect" action="https://test.ccavenue.com/transaction/transaction.do?command=initiateTransaction" > 
                    <input type="hidden" id="encRequest" name="encRequest" value=$encReq>
                    <input type="hidden" name="access_code" id="access_code" value=$xscode>
                    <script language='javascript'>document.redirect.submit();</script>
            </form>    
            </body>
            </html>
            '''
        # fin = Template(html).safe_substitute(encReq=encryption,xscode=accessCode)
        context = {
            "encReq": encryption,
            "xscode": accessCode,
        }
        return render(request, 'redirectPage.html', context=context)