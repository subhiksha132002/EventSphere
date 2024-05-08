from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('events/', views.events_view, name='events'),
    path('event_categories/', views.event_categories_view, name='event_categories'), 
    path('events/create_event/', views.create_event_view, name='create_event'),
    path('events/create_event/create/', views.create_event, name='create_event_submit')
]
