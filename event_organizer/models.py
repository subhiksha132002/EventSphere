from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField


class Attendee(models.Model):
    ATTENDANCE_CHOICES = [
        ('attended', 'Attended'),
        ('not_attended', 'Not Attended'),
    ]
    attendee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey('admin_panel.Event', on_delete=models.CASCADE,related_name='event_organizer_attendees')
    status = models.CharField(max_length=20, choices=ATTENDANCE_CHOICES, default='not_attended')
    name = models.CharField(max_length=100)  
    phone_number = PhoneNumberField()

    def __str__(self):
        return f"{self.attendee.username} - {self.event.name}"