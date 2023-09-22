import os
from celery import Celery
from django.conf import settings
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main_pro.settings')

app = Celery('main_pro')

# Including the beat schedule in the configuration directly
celery_schedule = {
    'archive_old_records_task': {
        'task': 'netmagics.tasks.simple_task',
        'schedule': timedelta(minutes=2),
    },
}

app.conf.beat_schedule = celery_schedule

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)







# import os
# from celery import Celery
# from django.conf import settings
# from datetime import timedelta



# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main_pro.settings')

# app = Celery('main_pro')

# app.config_from_object('django.conf:settings', namespace='CELERY')
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)



# CELERY_BEAT_SCHEDULE = {
#     'archive_old_records_task': {
#         'task': 'netmagics.oldrecords.archive_old_records',  # Make sure to adjust with your app name and module.
#         'schedule': timedelta(minutes=2),  # This sets the task to run every day.
#     },
# }