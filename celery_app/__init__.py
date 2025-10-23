from celery import Celery
from app.config import settings

app = Celery('presentation_generator')
app.config_from_object('celery_app.celery_config')

# Import tasks to ensure they're registered
from celery_app import tasks