import os

from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.dev")

app = Celery("core")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.update(CELERY_IMPORTS=("tasks",))
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
