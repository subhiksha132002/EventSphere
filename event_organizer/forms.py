from django import forms
from admin_panel.models import Event
from accounts.models import CustomUser

class EventForm(forms.ModelForm):
    attendees = forms.ModelMultipleChoiceField(queryset=CustomUser.objects.all(), required=False)  # Add attendees field

    class Meta:
        model = Event
        fields = ['name', 'description', 'event_category', 'location', 'date_time', 'image','ticket_type', 'ticket_price', 'attendees']

class EditEventForm(forms.ModelForm):
    attendees = forms.ModelMultipleChoiceField(queryset=CustomUser.objects.all(), required=False)
    class Meta:
        model = Event
        fields = ['name', 'description', 'event_category', 'location', 'date_time', 'image','ticket_type', 'ticket_price','attendees']
        widgets = {
            'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
