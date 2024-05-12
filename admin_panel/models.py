from django.db import models
from accounts.models import CustomUser
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings

class EventCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    total_events = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    event_category = models.ForeignKey(EventCategory, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    date_time = models.DateTimeField()
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    attendees = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='attended_events')

    def __str__(self):
        return self.name

    def is_completed(self):
        return self.date_time < timezone.now()

    @property
    def completed_events(self):
        return Event.objects.filter(date_time__lt=timezone.now())

class EventOrganizer(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    events_organized = models.ManyToManyField('admin_panel.Event', related_name='organizers', blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    phone_number = PhoneNumberField(blank=True)

    def __str__(self):
        return self.user.username