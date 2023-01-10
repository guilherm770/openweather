from celery import current_app as current_celery_app
from .config import settings


def create_celery():
    celery_app = current_celery_app
    celery_app.config_from_object(settings, namespace='CELERY')
    celery_app.conf.update(task_track_started=True)
    celery_app.conf.update(task_ignore_result=True)
    celery_app.conf.update(task_acks_late=True)
    celery_app.conf.update(worker_max_tasks_per_child=200)
    celery_app.conf.update(worker_send_task_events=True)
    celery_app.conf.update(worker_prefetch_multiplier=1)

    return celery_app