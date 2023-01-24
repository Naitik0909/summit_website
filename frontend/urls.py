from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('events/', views.EventsPageView.as_view(), name='events'),
    path('guests/', views.GuestsPageView.as_view(), name='guests'),
    path('prizes/', views.PrizesPageView.as_view(), name='prizes'),
    path('gallery/', views.GalleryPageView.as_view(), name='gallery'),
    path('about/', views.AboutUsView.as_view(), name='about'),
    path('team_and_contact/', views.TeamAndContactPageView.as_view(), name='team_and_contact'),
    path('scores_and_fixtures/', views.ScoresAndFixturesPageView.as_view(), name='scores_and_fixtures'),
    path('sport_detail/<pk>', views.SportDetailPageView.as_view(), name='sport_detail'),
    path('sport_register/<pk>', views.SportRegisterPageView.as_view(), name='sport_register'),
    path('update_team/<pk>', views.UpdateTeamPage.as_view(), name='update_team')

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)