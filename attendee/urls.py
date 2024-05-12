from django.urls import path
from . import views

app_name = 'attendee'

urlpatterns = [
    path('home/', views.home, name='home')
    ]