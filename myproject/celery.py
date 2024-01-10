import os
from celery import Celery
from myproject import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
app = Celery('myproject')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Automatically discover tasks in your Django app
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# Define periodic tasks (if needed)
app.conf.beat_schedule = {
    'print_hello': {
        'task': 'NotificationView',  # Replace with your actual task name
        'schedule': 1.0
    }
}

# Define some example tasks (can be removed if not needed)
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
    print("Hello From Celery")

@app.task
def print_hello():
    print("Hello From Celery Function")
