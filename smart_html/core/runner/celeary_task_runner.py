from celery import Celery

from .base import TaskRunner

class CeleryTaskRunner(TaskRunner):
    def __init__(self, name, broker):
        self.celery_app = Celery(name, broker=broker)

    def submit_task(self, task, *args, **kwargs):
        self.celery_app.send_task(task.__name__, args=args, kwargs=kwargs)
