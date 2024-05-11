from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db import transaction
from django.contrib.auth.decorators import login_required
from .models import Event, EventCategory, EventOrganizer
from accounts.models import CustomUser
from .forms import EventForm,EditEventForm,EventCategoryForm,EditCategoryForm,UserForm,EditUserForm,EventOrganizerForm,EditOrganizerForm
from django.utils import timezone
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse,HttpResponseRedirect
import logging

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

    return render(request, 'create_event.html', {
        'form': form,
        'event_categories': event_categories,
        'attendees': attendees,  # Pass the attendees to the template context
        'active_page': 'events'  # Set the active_page context variable to 'events'
    })

def edit_event_view(request, event_id):
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
    return render(request, 'edit_event.html', context)



# Function to retrieve event category page
def event_categories_view(request):
    all_categories = EventCategory.objects.all()
    return render(request, 'event_categories.html', {'active_page': 'event_categories', 'all_categories': all_categories})

def create_category(request):
    if request.method == 'POST':
        form = EventCategoryForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = EventCategoryForm()

    active_page = 'event_categories'
    return render(request, 'create_category.html', {'form': form, 'active_page': active_page})

def edit_category(request, category_id):
    category = get_object_or_404(EventCategory, id=category_id)
    if request.method == 'POST':
        form = EventCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            # Redirect to a success page or another view
    else:
        form = EventCategoryForm(instance=category)
    active_page = 'event_categories'
    return render(request, 'edit_category.html', {'form': form, 'category': category, 'active_page': active_page})

    
def delete_category(request, category_id):
    category = get_object_or_404(EventCategory, id=category_id)
    if request.method == 'POST':
        category.delete()
        # Redirect to the event categories list or another appropriate page
        return redirect(reverse('admin_panel:event_categories'))
    active_page = 'event_categories'
    return render(request, 'delete_category.html', {'category': category, 'active_page': active_page})

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
    events = Event.objects.all()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            events_attending = form.cleaned_data.get('events_attending')
            user.save()
            user.events_attending.set(events_attending)
            success_message = 'User created successfully.'
            return JsonResponse({'success': success_message}, status=200)
        else:
            error_message = 'Failed to create user. Please check the form data.'
            return JsonResponse({'error': error_message}, status=400)
    else:
        form = UserForm(initial={'events_attending': events})
        active_page = 'users'
        context = {
            'form': form,
            'active_page': active_page,
            'events': events,
        }
        return render(request, 'create_attendee.html', context)
      
def edit_user_view(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            events_attending = form.cleaned_data.get('events_attending')
            user.save()
            user.events_attending.set(events_attending)
            # Redirect to a success page or another view
            return redirect('success_url')
    else:
        form = EditUserForm(instance=user)

    active_page = 'users'
    return render(request, 'edit_user.html', {'form': form, 'active_page': active_page})


def event_organizers_view(request):
    organizers_with_events = {}  # Initialize an empty dictionary to store organizers and their events
    organizers = EventOrganizer.objects.all()
    for organizer in organizers:
        # Retrieve events organized by the organizer
        events = organizer.events_organized.all()
        organizers_with_events[organizer] = events
    context = {
        'organizers_with_events': organizers_with_events,
    }
    return render(request, 'event_organizers.html', context)
def create_organizer(request):
    if request.method == 'POST':
        form = EventOrganizerForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': 'Organizer created successfully.'}, status=200)
        else:
            return JsonResponse({'error': 'Failed to create organizer. Please check the form data.'}, status=400)
    else:
        form = EventOrganizerForm()

    active_page = 'event_organizers'
    return render(request, 'create_organizer.html', {'form': form, 'active_page': active_page})
def edit_organizer_view(request, organizer_id):
    organizer = get_object_or_404(EventOrganizer, id=organizer_id)

    if request.method == 'POST':
        form = EditOrganizerForm(request.POST, instance=organizer.user)
        if form.is_valid():
            form.save()
            # Redirect to a success page or another view
            return redirect('success_url')
    else:
        form = EditOrganizerForm(instance=organizer.user)

    active_page = 'event_organizers'
    return render(request, 'edit_organizer.html', {'form': form, 'active_page': active_page})

