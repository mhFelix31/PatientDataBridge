from celery import Celery

app = Celery('patient-data-bridge')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
