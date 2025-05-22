import os
from celery import Celery
from celery.schedules import crontab  # <-- ADD THIS

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'billing_project.settings')

app = Celery('billing_project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Celery Beat schedule
app.conf.beat_schedule = {
    'generate-daily-invoices': {
        'task': 'billing.tasks.generate_invoices',
        'schedule': crontab(minute=0, hour=0),  # every day at midnight
    },
}
