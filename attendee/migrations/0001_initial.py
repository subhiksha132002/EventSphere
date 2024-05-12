# Generated by Django 5.0.4 on 2024-05-12 15:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('admin_panel', '0003_event_ticket_price_event_ticket_type'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qr_code', models.ImageField(upload_to='qr_codes/')),
                ('ticket_type', models.CharField(max_length=100)),
                ('ticket_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('attendee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets_attendee', to=settings.AUTH_USER_MODEL)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_panel.event')),
            ],
        ),
        migrations.CreateModel(
            name='Attendee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=15)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_panel.event')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendee_user', to=settings.AUTH_USER_MODEL)),
                ('tickets', models.ManyToManyField(related_name='attendees', to='attendee.ticket')),
            ],
        ),
    ]