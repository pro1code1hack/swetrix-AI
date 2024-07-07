from celery import Celery

celery_app = Celery(
    "swetrix-ai-celery",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)

celery_app.conf.update(
    result_expires=3600,
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    task_soft_time_limit=3600,  # 1 hour soft time limit
    task_time_limit=3700,  # 1 hour 10 minutes hard time limit
)

from celery_tasks.tasks import *

# celery_app.autodiscover_tasks(['celery_tasks'])
