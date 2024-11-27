from celery import shared_task
from django.utils import timezone
from .models import Task

@shared_task
def print_task_details():
    # Fetch tasks added by user with id=1
    tasks = Task.objects.filter(user_id=1)

    # Log task details
    for task in tasks:
        # This will log the task details in the Celery worker log
        print(f"Task Title: {task.title}, Duration: {task.duration}, Created At: {task.created_at}")
