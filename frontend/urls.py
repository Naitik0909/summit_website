from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view()),
    path('events/', views.EventsPageView.as_view()),
    path('guests_and_prices/', views.GuestsAndPricesPageView.as_view()),
    path('team_and_contact/', views.TeamAndContactPageView.as_view()),
    path('scores_and_fixtures/', views.ScoresAndFixturesPageView.as_view()),
]