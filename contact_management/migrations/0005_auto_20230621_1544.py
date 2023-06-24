from django.db import migrations


def set_position(apps, schema_editor):
    Contact = apps.get_model('contact_management', 'Contact')
    Reminder = apps.get_model('contact_management', 'Reminder')
    for contact in Contact.objects.all():
        reminders = list(contact.reminder_set.order_by('date_time'))
        for i, reminder in enumerate(reminders):
            reminder.position = i
            reminder.save()


class Migration(migrations.Migration):
    dependencies = [
        ('contact_management', '0004_reminder_position'),
    ]

    operations = [
        migrations.RunPython(set_position),
    ]
