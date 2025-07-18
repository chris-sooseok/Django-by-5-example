import os
from celery import Celery
from online_shop import settings

# set the default Django settings module for the 'celery' program.
# You set the DJANGO_SETTINGS_MODULE variable for the Celery command-line program.
os.environ.setdefault(('DJANGO_SETTINGS_MODULE'), '3-online-shop.settings')

# You create an instance of the application with app = Celery('3-online-shop').
app = Celery('3-online-shop')

# You load any custom configuration from your project settings using the config_from_object() method
app.config_from_object('django.conf:settings', namespace='CELERY')

# tell Celery to auto-discover asynchronous tasks.py for your apps
# celery looks for tasks.py.py file in each app aaded to INSTALLED_APPS
app.autodiscover_tasks()

