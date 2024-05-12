from django.urls import path

from . import views

def is_event_organizer(user):
    return user.user_type == 'organizer'

app_name = 'event_organizer'

urlpatterns = [
    path('organizer_dashboard/', views.dashboard_view, name='dashboard'),
    path('events/', views.events_view, name='events'),
    path('events/create_event/', views.create_event, name='create_event'),
    path('events/<int:event_id>/edit_event/', views.edit_event, name='edit_event'),
    path('events/<int:event_id>/delete/', views.delete_event, name='event_delete')
]