from celery import Celery


import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'starwars_test_task.settings')
app = Celery('starwars_test_task')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


