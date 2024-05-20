from django.urls import path
from . import views

app_name = 'attendee'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('create_event_organizer/', views.event_organizer_form, name='create_event_organizer'),
    path('events/', views.events_list, name='events_list'),
    path('events/<int:event_id>/', views.event_detail, name='event_details'),
     path('generate_ticket/', views.generate_pdf, name='generate_ticket'),
    path('registration/', views.registration_view, name='registration'),
    ]