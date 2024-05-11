from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('attendee', 'Attendee'),
        ('organizer', 'Event Organizer'),
        ('admin', 'Administrator'),
    )
    USER_STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='attendee')
    events_attending = models.ManyToManyField('admin_panel.Event', related_name='attending_users')
    user_status = models.CharField(max_length=20, choices=USER_STATUS_CHOICES, default='active')

    def __str__(self):
        return self.username
