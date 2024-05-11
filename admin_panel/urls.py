from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('events/', views.events_view, name='events'),
    path('event_categories/', views.event_categories_view, name='event_categories'), 
    path('events/create_event/', views.create_event, name='create_event'),
    path('events/<int:event_id>/edit_event/', views.edit_event_view, name='edit_event'),
    path('event_categories/create_category/', views.create_category, name='create_category'),
    path('event_categories/<int:category_id>/edit_category/', views.edit_category, name='edit_category'),
    path('event_categories/<int:category_id>/delete_category/', views.delete_category, name='delete_category'),
    path('users/', views.users_view, name='users'),
    path('users/create_user/', views.create_user_view, name='create_user'),
    path('users/<int:user_id>/edit_user/', views.edit_user_view, name='edit_user'),
    path('event_organizers/', views.event_organizers_view, name='event_organizers'),
    path('event_organizers/create_organizer/', views.create_organizer, name='create_organizer'),
    path('event_organizers/<int:organizer_id>/edit_organizer/', views.edit_organizer_view, name='edit_organizer'),

]
