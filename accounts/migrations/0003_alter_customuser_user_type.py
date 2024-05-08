# Generated by Django 5.0.4 on 2024-05-08 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_customuser_events_attending_customuser_groups_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[('admin', 'Admin'), ('organizer', 'Event Organizer'), ('attendee', 'Attendee')], max_length=20),
        ),
    ]