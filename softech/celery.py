import os
from celery import Celery
from django.conf import settings


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "softech.settings")
app = Celery("softech")
app.config_from_object('softech.settings', namespace="CELERY")
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):  
    print(f"Request: {self.request!r}")

