from django.contrib import admin
from django.contrib.auth.models import User
from .models import Event,Attendee

admin.site.register(User)
admin.site.register(Event)
admin.site.register(Attendee)

