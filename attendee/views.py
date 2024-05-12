from django.shortcuts import render
from admin_panel.models import Event
from django.core.mail import send_mail
from .forms import EventOrganizerForm

def home(request):
    # Assuming you have a model named Event with fields: name, description, location, date_time
    # Querying the latest events
    latest_events = Event.objects.all().order_by('-date_time')[:3]  # Assuming you want to display the latest 3 events

    context = {
        'latest_events': latest_events,
    }
    return render(request, 'home.html', context)

def event_organizer_form(request):
    if request.method == 'POST':
        form = EventOrganizerForm(request.POST)
        if form.is_valid():
            # Get form data
            full_name = form.cleaned_data['full_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            college_name = form.cleaned_data['college_name']
            department = form.cleaned_data['department']
            additional_notes = form.cleaned_data['additional_notes']
            
            # Send email to admin
            send_mail(
                'New Event Organizer Request',
                f'Name: {full_name}\nEmail: {email}\nPhone: {phone_number}\nCollege: {college_name}\nDepartment: {department}\nNotes: {additional_notes}',
                'your_email@example.com',
                ['admin@example.com'],
                fail_silently=False,
            )
            # Redirect to a success page or show a success message
            return render(request, 'success.html')
    else:
        form = EventOrganizerForm()
    return render(request, 'create_event_organizer.html', {'form': form})
