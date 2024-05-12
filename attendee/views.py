from django.shortcuts import render
from admin_panel.models import Event

def home(request):
    # Assuming you have a model named Event with fields: name, description, location, date_time
    # Querying the latest events
    latest_events = Event.objects.all().order_by('-date_time')[:3]  # Assuming you want to display the latest 3 events

    # Sample content about the website
    website_content = "Welcome to EventSphere! Your ultimate destination for discovering and participating in exciting events. Whether you're looking for workshops, conferences, or social gatherings, we have something for everyone."

    context = {
        'latest_events': latest_events,
        'website_content': website_content,
    }
    return render(request, 'home.html', context)
