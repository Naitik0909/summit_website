from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('events/', views.EventsPageView.as_view(), name='events'),
    path('guests_and_prices/', views.GuestsAndPricesPageView.as_view(), name='guests_and_prices'),
    path('team_and_contact/', views.TeamAndContactPageView.as_view(), name='team_and_contact'),
    path('scores_and_fixtures/', views.ScoresAndFixturesPageView.as_view(), name='scores_and_fixtures'),
]