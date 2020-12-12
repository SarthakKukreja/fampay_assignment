import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fampay_assignment.settings')
app = Celery('fampay_assignment')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Celery beat acts as schedular to execute code every t seconds.
# Can be configured as env variable.
app.conf.beat_schedule = {
    'every-30-seconds': {
        'task': 'youtube_search.tasks.updateDatabase',
        'schedule': 30,
    }
}

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
