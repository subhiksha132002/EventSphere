from django.urls import path
from . import views


app_name = 'accounts'

urlpatterns = [
    path('registration/', views.registration_view, name='registration'),
    
    # Add other URLs for admin, organizer, and attendee dashboards
]