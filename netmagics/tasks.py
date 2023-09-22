# from django.core.management.base import BaseCommand
# from netmagics.models import ActivityTracker
# import csv
# from datetime import timedelta
# from django.utils import timezone
# import os  # <-- Added import here

# class Command(BaseCommand):
#     help = 'Archive old records from ActivityTracker to a CSV file.'

#     def handle(self, *args, **kwargs):
#         # Check and create 'archives/' directory if it doesn't exist
#         if not os.path.exists('archives'):
#             os.makedirs('archives')  # This will create the 'archives/' directory

#         expiry_time = timezone.now() - timedelta(days=3)  # Adjust as needed

#         # Filter records older than the expiry time
#         old_records = ActivityTracker.objects.filter(time__lt=expiry_time)

#         # Define the CSV file path
#         csv_path = f'archives/{expiry_time.date()}.csv'

#         # Write records to the CSV file
#         with open(csv_path, 'w', newline='') as csvfile:
#             fieldnames = ['time', 'description', 'done_by']
#             writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

#             writer.writeheader()
#             for record in old_records:
#                 writer.writerow({
#                     'time': record.time,
#                     'description': record.description,
#                     'done_by': record.done_by
#                 })

#         # Delete archived records from the database
#         old_records.delete()

#         self.stdout.write(self.style.SUCCESS(f'Successfully archived {old_records.count()} records to {csv_path}'))










from celery import shared_task
from .models import ActivityTracker
import csv
from datetime import timedelta
from django.utils import timezone
import os

@shared_task
def archive_old_records():
    # Check and create 'archives/' directory if it doesn't exist
    if not os.path.exists('archives'):
        os.makedirs('archives')  # This will create the 'archives/' directory

    expiry_time = timezone.now() - timedelta(days=2)  # Adjust as needed

    # Filter records older than the expiry time
    old_records = ActivityTracker.objects.filter(time__lt=expiry_time)

    # If there are no old records, we can exit early
    if not old_records.exists():
        return "No old records to archive."

    # Define the CSV file path
    csv_path = f'archives/{expiry_time.date()}.csv'

    # Write records to the CSV file
    with open(csv_path, 'w', newline='') as csvfile:
        fieldnames = ['time', 'description', 'done_by']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for record in old_records:
            writer.writerow({
                'time': record.time,
                'description': record.description,
                'done_by': record.done_by
            })

    # Count the archived records for the response
    count = old_records.count()

    # Delete archived records from the database
    old_records.delete()

    return f"Successfully archived {count} records to {csv_path}."

@shared_task
def simple_task():
    return "Simple task executed!"