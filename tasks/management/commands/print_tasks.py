# tasks/management/commands/print_tasks.py

from django.core.management.base import BaseCommand
from tasks.models import Task
import logging
from time import sleep

# Set up logging configuration
logger = logging.getLogger('django')

class Command(BaseCommand):
    help = 'Print all tasks in the database with a 10-second delay between each.'

    def handle(self, *args, **kwargs):
        tasks = Task.objects.all()  # Fetch all tasks from the database
        
        for task in tasks:
            # Log task details (this will be displayed in the terminal/console)
            logger.info(f"Task Title: {task.title}, Duration: {task.duration}, Created At: {task.created_at}")
            sleep(10)  # Wait for 10 seconds between tasks
