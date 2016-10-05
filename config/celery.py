import os

from celery import Celery

import environ

from django.conf import settings  # noqa

ROOT_DIR = environ.Path(__file__)  - 2
APPS_DIR = ROOT_DIR.path('dc_traffic_tickets')
env = environ.Env()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', env('DJANGO_SETTINGS_MODULE'))
app = Celery('trafficsite')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
