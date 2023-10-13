import os

from celery import Celery

# Establish the module of default settings of django to celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')

app = Celery('myshop')
app.config_from_object('django.conf:settings', namespace='CELERY')
# Find the async tasks automatically
# Celery will find out a file called tasks.py in every folder of
# every app which is in iNSTALLED_APPS
app.autodiscover_tasks()
