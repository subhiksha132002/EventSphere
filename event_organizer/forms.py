from django import forms
from admin_panel.models import Event
from accounts.models import CustomUser

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'event_category', 'location', 'date_time', 'image','ticket_type', 'ticket_price']

class EditEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'event_category', 'location', 'date_time', 'image','ticket_type', 'ticket_price']
        widgets = {
            'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        labels = {
            'ticket_type': 'Registration Type',
            'ticket_price': 'Registration Fee',
        }
