# Generated by Django 5.0.4 on 2024-05-12 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_organizer', '0003_alter_attendee_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendee',
            name='status',
            field=models.CharField(choices=[('attended', 'Attended'), ('not_attended', 'Not Attended')], default='not_attended', max_length=20),
        ),
    ]
