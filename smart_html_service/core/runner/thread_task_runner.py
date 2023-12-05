import threading

from .base import TaskRunner

class ThreadTaskRunner(TaskRunner):
    def submit_task(self, task, *args, **kwargs):
        thread = threading.Thread(target=task, args=args, kwargs=kwargs)
        thread.start()