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
        queryset=Event.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'date_joined', 'user_type', 'events_attending','status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['events_attending'].initial = self.instance.events_attending.all()
            
class EditUserForm(forms.ModelForm):
    events_attending = forms.ModelChoiceField(
        queryset=Event.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'date_joined', 'user_type', 'events_attending']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['events_attending'].initial = self.instance.events_attending.all()

class EventOrganizerForm(UserCreationForm):
    email = forms.EmailField()
    events = forms.ModelChoiceField(queryset=Event.objects.all(), empty_label="Select Event", required=False)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'username', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            event = self.cleaned_data.get('events')
            if event:
                organizer = EventOrganizer.objects.create(user=user)
                organizer.events_organized.add(event)
        return user

    
class EditOrganizerForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            # Customize the initialization if needed
            pass
