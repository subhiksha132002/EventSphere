# Generated by Django 5.0.4 on 2024-05-11 04:57

import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventorganizer',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None),
        ),
        migrations.AddField(
            model_name='eventorganizer',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending', max_length=20),
        ),
        migrations.AlterField(
            model_name='eventorganizer',
            name='events_organized',
            field=models.ManyToManyField(blank=True, related_name='organizers', to='admin_panel.event'),
        ),
    ]
