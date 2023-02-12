from django.conf import settings
from pay_ccavenue import CCAvenue

def listToString(s):
 
    # initialize an empty string
    str1 = ""
 
    # traverse in the string
    for ele in s:
        str1 += ele
        str1 += ", "
 
    # return string
    return str1[:-2]

def stringToBool(s):
    if s == 'yes':
         return True
    else:
        return False

def addGST(price):
    try:
        cal_price = float(price)
        return cal_price + (cal_price * 0.18)
    except:
        return price

def initiatePayment(player_emails, team):
    # Send request to payment gateway
    sport = team.sport
    order_id = team.order_id
    basePrice = 0
    if(team.is_male_team):
        basePrice = sport.priceMale
    else:
        basePrice = sport.priceFemale
    
    if("Swimming" in sport.name):
        basePrice = basePrice * len(player_emails)

    reqObj = {
        'merchant_id': settings.CC_AVENUE_MERCHANT_ID,
        'order_id': order_id,
        'currency': settings.CC_AVENUE_CURRENCY,
        'redirect_url':settings.CC_AVENUE_SUCCESS_URL,
        'cancel_url': settings.CC_AVENUE_FAILURE_URL,
        'language': settings.CC_AVENUE_LANG,
        'amount': basePrice,
    }
    ccavenue = CCAvenue()
    encrypt_data = ccavenue.encrypt(reqObj)
    context = {
        "encReq": encrypt_data,
        "xscode": settings.CC_AVENUE_ACCESS_CODE,
        "ccAveURL": settings.CC_AVENUE_URL
    }
    return context

def reduceArray(arr,n):
    newArr = []
    for i in range(0,n):
        newArr.append(arr[i])
    return newArr