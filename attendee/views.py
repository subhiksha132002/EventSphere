from django.shortcuts import render,get_object_or_404,redirect
from admin_panel.models import Event,EventCategory
from django.core.mail import send_mail
from django.utils import timezone
from .forms import EventOrganizerForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate


def home(request):
    latest_events = Event.objects.filter(date_time__gte=timezone.now()).order_by('-date_time')[:4]
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

def events_list(request):
    all_events = Event.objects.all()  
    categories = EventCategory.objects.all()
    context = {
        'all_events': all_events,
        'categories': categories,
    }
    return render(request, 'events_list.html', context)

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'event_detail.html', {'event': event})

def registration_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('attendee:events_list')  # Redirect to events list page after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'registration.html', {'form': form})