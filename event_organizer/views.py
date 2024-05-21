from django.shortcuts import render, redirect, get_object_or_404
from admin_panel.models import Event
from .models import  Attendee
from django.utils import timezone
from .forms import EventForm,EditEventForm
from admin_panel.models import EventCategory
from accounts.models import CustomUser

# Views for Event Organizer Dashboard
def dashboard_view(request):
    # Retrieve data for the dashboard for the logged-in event organizer
    logged_in_organizer = request.user
    total_events = Event.objects.filter(organizer=logged_in_organizer).count()
    total_completed_events = Event.objects.filter(organizer=logged_in_organizer, date_time__lt=timezone.now()).count()
    total_attendees = Attendee.objects.filter(event__organizer=logged_in_organizer).count()
    latest_events = Event.objects.filter(organizer=logged_in_organizer).order_by('-date_time')[:5]

    # Pass data to the template
    context = {
        'total_events': total_events,
        'total_completed_events': total_completed_events,
        'total_attendees': total_attendees,
        'latest_events': latest_events,
        'active_page': 'dashboard'
    }
    return render(request, 'organizer_base.html', context)

# Function to retrieve events
def events_view(request):
    all_events = Event.objects.all()
    return render(request, 'organizer_events.html', {'active_page': 'events', 'all_events': all_events})

def create_event(request):
    event_categories = EventCategory.objects.all()  # Retrieve all event categories
    attendees = CustomUser.objects.all()  # Retrieve all attendees
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        event = form.save(commit=False)
        event.organizer = request.user
        event.save()
        form.save_m2m()
            
            # Handle attendees field
        attendee_ids = request.POST.getlist('attendees')
        event.attendees.set(attendee_ids)
    else:
        form = EventForm()

    return render(request, 'organizer_create_event.html', {
        'form': form,
        'event_categories': event_categories,
        'attendees': attendees,  # Pass the attendees to the template context
        'active_page': 'events'  # Set the active_page context variable to 'events'
    })

def edit_event(request, event_id):
    # Retrieve existing event
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        # Handle form submission
        form = EditEventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()

    else:
        # Pre-populate form fields with event data
        form = EditEventForm(instance=event)

    # Pass 'active_page' context variable
    context = {'form': form, 'event': event, 'active_page': 'events'}
    return render(request, 'organizer_edit_event.html', context)

def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event.delete()
    return redirect('event_organizer:organizer_events')  # Redirect to the events page after deletion

# Function to retrieve attendees
def attendees_view(request):
    # Retrieve the logged-in event organizer
    logged_in_organizer = request.user

    # Retrieve all attendees for events organized by the logged-in organizer
    all_attendees = Attendee.objects.filter(event__organizer=logged_in_organizer)

    # Pass the attendees data to the template
    context = {
        'all_attendees': all_attendees,
        'active_page': 'attendees'
    }
    return render(request, 'organizer_attendees.html', context)