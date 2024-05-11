from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Event,EventCategory,CustomUser,EventOrganizer

class EventForm(forms.ModelForm):
    attendees = forms.ModelMultipleChoiceField(queryset=CustomUser.objects.all(), required=False)  # Add attendees field

    class Meta:
        model = Event
        fields = ['name', 'description', 'event_category', 'location', 'date_time', 'image', 'attendees']
class EditEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'event_category', 'location', 'date_time', 'image']
        widgets = {
            'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
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
    events_attending = forms.ModelMultipleChoiceField(
        queryset=Event.objects.none(),  # Set an empty queryset initially
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=False
    )
    user_status = forms.ChoiceField(choices=CustomUser.USER_STATUS_CHOICES)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'username', 'email', 'date_joined', 'user_type', 'user_status', 'events_attending']

    def __init__(self, *args, **kwargs):
        queryset = kwargs.pop('queryset', Event.objects.none())  # Set a default empty queryset
        super().__init__(*args, **kwargs)
        self.fields['events_attending'].queryset = queryset

class EditUserForm(forms.ModelForm):
    events_attending = forms.ModelMultipleChoiceField(
        queryset=Event.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'date_joined', 'user_type', 'user_status', 'events_attending']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['events_attending'].initial = self.instance.events_attending.all()
            
from django import forms
from .models import CustomUser, EventOrganizer, Event

class EditOrganizerBasicForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'username', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['first_name'].initial = self.instance.first_name
            self.fields['username'].initial = self.instance.username
            self.fields['email'].initial = self.instance.email

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
        fields = ['status', 'phone_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

