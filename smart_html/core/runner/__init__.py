from flask import Flask

from .celeary_task_runner import CeleryTaskRunner
from .thread_task_runner import ThreadTaskRunner

def init_runner(app: Flask):
    celery_broker = app.config.get("CELERY_BROKER", "")
    if celery_broker != "":
        app.task_runner = ThreadTaskRunner()
    else:
        app.task_runner = CeleryTaskRunner("smart_html_runner", celery_broker)
