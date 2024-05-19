from django.urls import path
from . import views

app_name = 'attendee'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('create_event_organizer/', views.event_organizer_form, name='create_event_organizer'),

    ]