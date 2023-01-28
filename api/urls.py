from django.urls import path
from . import views

urlpatterns = [
    path('payment_form/', views.PaymentForm.as_view(), name="payment"),
    path('ccavRequestHandler/', views.CCAveReqeustHandler.as_view(), name="ccave_request_handler"),
]
