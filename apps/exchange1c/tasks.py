from celery.exceptions import Reject
from django.core import management
from system import celery_app


@celery_app.task()
def import_1c_task(filename):
    try:
        management.call_command('parse', in_action=1, filename=filename)
        print('Sended.')

    except MemoryError as exc:
        raise Reject(exc, requeue=False)
