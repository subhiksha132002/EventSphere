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
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.views.generic import View
from .decorators import admin_required


@admin_required
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
    return render(request, 'index.html',context)

@admin_required
# Function to retrieve event page
def events_view(request):
    all_events = Event.objects.all()
    return render(request, 'events.html', {'active_page': 'events', 'all_events': all_events})

@admin_required
def create_event(request):
    event_categories = EventCategory.objects.all()  # Retrieve all event categories
    attendees = CustomUser.objects.all()  # Retrieve all attendees
    
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user  # Assign the authenticated user as the organizer
            event.save()
            form.save_m2m()
            
            # Handle attendees field
            attendee_ids = request.POST.getlist('attendees')
            event.attendees.set(attendee_ids)
            
            return redirect('admin_panel:events')  # Redirect to event detail page
    else:
        form = EventForm()

    return render(request, 'create_event.html', {
        'form': form,
        'event_categories': event_categories,
        'attendees': attendees,
        'active_page': 'events'
    })

@admin_required
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

@admin_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event.delete()
    return redirect('admin_panel:events')  # Redirect to the events page after deletion

@admin_required
# Function to retrieve event category page
def event_categories_view(request):
    all_categories = EventCategory.objects.all()
    return render(request, 'event_categories.html', {'active_page': 'event_categories', 'all_categories': all_categories})

@admin_required
def create_category(request):
    if request.method == 'POST':
        form = EventCategoryForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = EventCategoryForm()

    active_page = 'event_categories'
    return render(request, 'create_category.html', {'form': form, 'active_page': active_page})

@admin_required
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

@admin_required   
def delete_category(request, category_id):
    category = get_object_or_404(EventCategory, id=category_id)
    category.delete()
    # Redirect to a success page or another appropriate URL
    return redirect('admin_panel:event_categories')

@admin_required
# Function to retrieve user page
def users_view(request):
    # Retrieve all CustomUser objects along with related data
    all_users = CustomUser.objects.all()

    context = {
        'active_page': 'users',  # Set active_page context variable
        'users': all_users,  # Pass the users data to the template
    }
    
    return render(request, 'attendees.html', context)
@admin_required
def create_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            if user.username:  # Ensure username is provided and not empty
                events_attending = form.cleaned_data.get('events_attending')
                user.save()
                user.events_attending.set(events_attending)
                success_message = 'User created successfully.'
                messages.success(request, success_message)
                return redirect('admin_panel:users')
            else:
                error_message = 'Username is required.'
                messages.error(request, error_message)
        else:
            error_message = 'Failed to create user. Please check the form data.'
            print(form.errors)  # Print form errors for debugging
            messages.error(request, error_message)
    else:
        queryset = Event.objects.all()  # Example queryset
        form = UserForm(queryset=queryset)  # Pass the queryset to the form

    context = {
        'form': form,
        'active_page': 'users',
    }
    return render(request, 'create_attendee.html', context)

@admin_required
def edit_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            events_attending = form.cleaned_data.get('events_attending')
            user.save()
            user.events_attending.set(events_attending)
            success_message = 'User updated successfully.'
            messages.success(request, success_message)
            return redirect('admin_panel:users')
    else:
        form = EditUserForm(instance=user)

    context = {
        'form': form,
        'user': user,
        'active_page': 'users'
    }
    return render(request, 'edit_user.html', context)

@admin_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('admin_panel:users')

@admin_required
def event_organizers_view(request):
    active_page = None
    organizers_with_events = {}  # Initialize an empty dictionary to store organizers and their events
    organizers = EventOrganizer.objects.all()
    for organizer in organizers:
        # Retrieve events organized by the organizer
        events = organizer.events_organized.all()
        organizers_with_events[organizer] = events
        active_page = 'event_organizers'
    context = {
        'organizers_with_events': organizers_with_events,
        'active_page': active_page,
    }
    return render(request, 'event_organizers.html', context)

from django.http import JsonResponse

User = get_user_model()

@admin_required
def create_organizer(request):
    if request.method == 'POST':
        form = EventOrganizerForm(request.POST)
        if form.is_valid():
            # Create a new User instance
            user_data = {
                'username': request.POST.get('username'),
                'email': request.POST.get('email'),
                'first_name': request.POST.get('first_name'),
                'user_type': 'organizer',
            }
            user = User.objects.create_user(**user_data)

            # Create an Organizer instance and associate it with the User
            organizer = form.save(commit=False)
            organizer.user = user
            organizer.save()
            form.save_m2m()  # Save the many-to-many relationships

            return JsonResponse({'success': 'Organizer created successfully.'}, status=200)
        return JsonResponse({'error': form.errors}, status=400)

    else:
        form = EventOrganizerForm()
        active_page = 'event_organizers'
        return render(request, 'create_organizer.html', {'form': form, 'active_page': active_page})

@admin_required           
def edit_organizer(request, organizer_id):
    organizer = get_object_or_404(EventOrganizer, id=organizer_id)

    if request.method == 'POST':
        form = EditOrganizerForm(request.POST, instance=organizer)
        if form.is_valid():
            form.save()
            organizer.phone_number = form.cleaned_data['phone_number']  # Update phone number
            organizer.save()
            return redirect('admin_panel:event_organizers')
    else:
        form = EditOrganizerForm(instance=organizer)

    active_page = 'event_organizers'
    context = {
        'form': form,
        'organizer': organizer,
        'active_page': active_page,
    }
    return render(request, 'edit_organizer.html', context)

@admin_required
def delete_organizer(request, organizer_id):
    organizer = get_object_or_404(EventOrganizer, id=organizer_id)
    organizer.delete()
    return redirect('admin_panel:event_organizers')

