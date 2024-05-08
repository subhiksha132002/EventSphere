from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db import transaction
from django.contrib.auth.decorators import login_required
from .models import Event, EventCategory, EventOrganizer
from accounts.models import CustomUser
from .forms import EventForm
from django.utils import timezone
from django.contrib import messages
import logging

# Create your views here.
# Views for Admin Dashboard
def dashboard_view(request):
    # Retrieve data for the dashboard
    total_events = Event.objects.count()
    total_categories = EventCategory.objects.count()
    total_organizers = EventOrganizer.objects.count()
    total_completed_events = Event.objects.filter(date_time__lt=timezone.now()).count()
    latest_events = Event.objects.order_by('-date_time')[:5]

    # Pass data to the template
    context = {
        'total_events': total_events,
        'total_categories': total_categories,
        'total_organizers': total_organizers,
        'total_completed_events': total_completed_events,
        'latest_events': latest_events,
        'active_page': 'dashboard'
    }
    return render(request, 'base.html',context)

# Function to retrieve event page
def events_view(request):
    all_events = Event.objects.all()
    return render(request, 'events.html', {'active_page': 'events', 'all_events': all_events})

# Function to retrieve event category page
def event_categories_view(request):
    all_categories = EventCategory.objects.all()
    return render(request, 'event_categories.html', {'active_page': 'event_categories', 'all_categories': all_categories})

def create_event_view(request):
    event_categories = EventCategory.objects.all()  # Retrieve all event categories
    return render(request, 'create_event.html', {
        'event_categories': event_categories,
        'active_page': 'events'  # Set the active_page context variable to 'events'
    })

def create_category_view(request):
    return render(request, 'create_category.html', {
        'active_page': 'event_categories'  
    })

logger = logging.getLogger(__name__)
@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            logger.info(f"Form data: {form.cleaned_data}")
            with transaction.atomic():
                event = form.save(commit=False)
                event.organizer = request.user
                event.save()
                form.save_m2m()
            event_data = {
                'name': event.name,
                'description': event.description,
                'category': str(event.event_category),
                'location': event.location,
                'date_time': str(event.date_time),
            }
            return JsonResponse(event_data, status=200)
        else:
            return JsonResponse({'error': 'Invalid form data'}, status=400)
    else:
        form = EventForm()
    return render(request, 'create_event.html', {'form': form})

@login_required
def create_category(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            logger.info(f"Form data: {form.cleaned_data}")
            with transaction.atomic():
                event = form.save(commit=False)
                event.organizer = request.user
                event.save()
                form.save_m2m()
            event_data = {
                'name': event.name,
                'description': event.description,
                'category': str(event.event_category),
                'location': event.location,
                'date_time': str(event.date_time),
            }
            return JsonResponse(event_data, status=200)
        else:
            return JsonResponse({'error': 'Invalid form data'}, status=400)
    else:
        form = EventForm()
    return render(request, 'create_category.html', {'form': form})


# Function to retrieve user page
def users_view(request):
    # Retrieve all CustomUser objects along with related data
    all_users = CustomUser.objects.all()

    context = {
        'active_page': 'users',  # Set active_page context variable
        'users': all_users,  # Pass the users data to the template
    }
    
    return render(request, 'attendees.html', context)

def create_user_view(request):
    return render(request, 'create_attendee.html', {
        'active_page': 'users'  
    })
def event_organizers_view(request):
    organizers = EventOrganizer.objects.all()

    # Create a dictionary to store the events organized by each organizer
    organizers_with_events = {}
    for organizer in organizers:
        # Get the events organized by the current organizer
        organized_events = organizer.events_organized.all()
        organizers_with_events[organizer] = organized_events

    context = {
        'organizers_with_events': organizers_with_events,
        'active_page': 'event_organizers'  # Move the 'active_page' key-value pair to the context dictionary
    }

    return render(request, 'event_organizers.html', context)  # Pass the context dictionary directly

def create_organizer_view(request):
    return render(request, 'create_organizer.html', {
        'active_page': 'event_organizers'  
    })
