from django import forms
from .models import Event,EventCategory,CustomUser,EventOrganizer

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

class EventCategoryForm(forms.ModelForm):
    class Meta:
        model = EventCategory
        fields = ['name', 'description']

class EditCategoryForm(forms.ModelForm):
    class Meta:
        model = EventCategory
        fields = ['name', 'description']  

    def __init__(self, *args, **kwargs):
        super(EditCategoryForm, self).__init__(*args, **kwargs)

class UserForm(forms.ModelForm):
    user_status = forms.ChoiceField(choices=CustomUser.USER_STATUS_CHOICES)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'username', 'email', 'date_joined', 'user_type', 'user_status']
        widgets = {
            'date_joined': forms.DateInput(attrs={'type': 'date'})
        }


    def __init__(self, *args, **kwargs):
        queryset = kwargs.pop('queryset', Event.objects.none())  # Set a default empty queryset
        super().__init__(*args, **kwargs)

class EditUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'date_joined', 'user_type', 'user_status']
        widgets = {
            'date_joined': forms.DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        

class EventOrganizerForm(forms.ModelForm):
    events_organized = forms.ModelMultipleChoiceField(
        queryset=Event.objects.all(),
        required=False,
        widget=forms.SelectMultiple,
        label="Events Organized"
    )

    class Meta:
        model = EventOrganizer
        fields = ['phone_number', 'status', 'events_organized']

class EditOrganizerForm(forms.ModelForm):
    class Meta:
        model = EventOrganizer
        fields = ['phone_number', 'status', 'events_organized']
        widgets = {
            'events_organized': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(EditOrganizerForm, self).__init__(*args, **kwargs)
        self.fields['events_organized'].queryset = Event.objects.all()


