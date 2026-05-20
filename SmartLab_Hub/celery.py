# Inside your Celery configuration
from celery import Celery
from celery.schedules import crontab

app = Celery('SmartLab_Hub')

app.conf.beat_schedule = {
    'daily-maintenance-check': {
        'task': 'alerts.tasks.check_maintenance_schedules',
        'schedule': crontab(hour=8, minute=0), # Runs every morning at 8am
    },
}