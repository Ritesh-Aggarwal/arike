import os
from datetime import timedelta

from django.conf import settings

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "arike.settings")
celery_app = Celery("arike")
celery_app.config_from_object("django.conf:settings")
celery_app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# celery_app.conf.update(BROKER_URL=os.environ['REDIS_URL'],
                # CELERY_RESULT_BACKEND=os.environ['REDIS_URL'])


# Periodic Task
# @periodic_task(run_every=timedelta(seconds=30))
# def every_30_seconds():
#     print("Running Every 30 Seconds!")