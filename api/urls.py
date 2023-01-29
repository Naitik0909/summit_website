from django.urls import path
from . import views

urlpatterns = [
    path('payment_form/', views.PaymentForm.as_view(), name="payment"),
    path('ccavRequestHandler/', views.CCAveReqeustHandler.as_view(), name="ccave_request_handler"),
    path('ccavResponseHandler/', views.CCAveResposeHandler.as_view(), name="ccave_response_handler"),
    path('validateSwimming/', views.validateSwimming, name="validate_swimming"),
]
