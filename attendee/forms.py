from django import forms

class EventOrganizerForm(forms.Form):
    full_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=15)
    college_name = forms.CharField(max_length=100)
    department = forms.CharField(max_length=100)
    additional_notes = forms.CharField(widget=forms.Textarea,required=False)