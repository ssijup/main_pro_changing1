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

    expiry_time = timezone.now() - timedelta(days=30)  # Adjust as needed
    print(expiry_time,'time ///')
    # Filter records older than the expiry time
    old_records = ActivityTracker.objects.filter(time__lt=expiry_time)

    # If there are no old records, we can exit early
    if not old_records.exists():
        return None,"No old records to archive."

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

    return csv_path,f"Successfully archived {count} records to {csv_path}."

@shared_task
def simple_task():
    return None,"Simple task executed!"