from django.contrib import admin
from django.contrib.auth.models import User
from .models import Event,EventCategory,EventOrganizer

admin.site.register(User)
admin.site.register(Event)
admin.site.register(EventCategory)
admin.site.register(EventOrganizer)