import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rd_l3_test.settings')

app = Celery('rd_l3_test')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'increase-debt-every-3-hours': {
        'task': 'network.tasks.increase_debt_task',
        'schedule': crontab(minute='0', hour='*/3'),
    },
    'decrease-debt-daily-630': {
        'task': 'network.tasks.decrease_debt_task',
        'schedule': crontab(minute='30', hour='6'),
    },
}
