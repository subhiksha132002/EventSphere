# Generated by Django 5.0.4 on 2024-05-14 12:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0003_event_ticket_price_event_ticket_type'),
        ('event_organizer', '0004_alter_attendee_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendee',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_organizer_attendees', to='admin_panel.event'),
        ),
        migrations.DeleteModel(
            name='Event',
        ),
    ]
