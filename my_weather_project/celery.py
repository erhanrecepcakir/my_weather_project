from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_weather_project.settings')


app = Celery('my_weather_project')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

"""
This periodic (beat scheduler) is commented out due to be added to Django database.
'django-celery-beat' package is loaded to project.

In admin panel, scheduler tasks can be managed in 'Home-Periodic Task' menu.
"""
# app.conf.beat_schedule = {
#     # Executes every day morning at 06:30.
#     'add-every-morning': {
#         'task': 'periodic_report_sender_to_subs_list',
#         'schedule': crontab(hour=6, minute=30),
#     },
# }

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))