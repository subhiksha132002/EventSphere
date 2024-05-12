from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from admin_panel.models import Event

class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    date_time = models.DateTimeField()
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    event_category = models.ForeignKey('admin_panel.EventCategory', on_delete=models.CASCADE, related_name='events')
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='organized_events')
    attendees = models.ManyToManyField(settings.AUTH_USER_MODEL, through='event_organizer.Attendee', related_name='organizer_attended_events')
    def __str__(self):
        return self.name

    def is_completed(self):
        return self.date_time < timezone.now()

    @property
    def completed_events(self):
        return Event.objects.filter(date_time__lt=timezone.now())


class Attendee(models.Model):
    attendee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.attendee.username} - {self.event.name}"