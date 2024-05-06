from django.urls import path
from . import views

urlpatterns = [
    path('hello/',views.admin_dashboard)
]