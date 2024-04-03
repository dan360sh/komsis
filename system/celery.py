import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'system.settings')

app = Celery('system')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


app.conf.beat_schedule = {
    'run-daily': {
        'task': 'apps.posts.tasks.mark_outdated_posts_as_inactive',
        'schedule': crontab(hour="*/3"),
    },
}

app.conf.timezone = 'UTC'
