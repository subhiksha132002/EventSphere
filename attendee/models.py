from django.db import models
from django.conf import settings
from admin_panel.models import Event as AdminPanelEvent

class Ticket(models.Model):
    event = models.ForeignKey(AdminPanelEvent, on_delete=models.CASCADE)
    attendee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tickets_attendee')
    qr_code = models.ImageField(upload_to='qr_codes/')
    ticket_type = models.CharField(max_length=100)
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Ticket {self.id} - {self.ticket_type}"

class Attendee(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='attendee_user')
    event = models.ForeignKey(AdminPanelEvent, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    # Remove the 'name' field
    tickets = models.ManyToManyField(Ticket, related_name='attendees')

    def __str__(self):
        return f"{self.user.first_name} - {self.event.name}"