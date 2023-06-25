# Sociosync/celery.py
from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SocioSync.settings')

app = Celery('SocioSync')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    'send-reminders': {
        'task': 'contact_management.tasks.send_reminders_task',
        'schedule': crontab(),  # Executes every minute.
    },
}
