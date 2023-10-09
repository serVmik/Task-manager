from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand

from task_manager.labels.models import Label
from task_manager.statuses.models import Status

from task_manager.fixtures.test_data import (
    users_data, statuses_data, labels_data, tasks_data
)
from task_manager.tasks.models import Task

User = get_user_model()


class Command(BaseCommand):
    help = "Add test data to database"

    def handle(self, *args, **options):
        for user_data in users_data:
            User.objects.get_or_create(
                username=user_data[0],
                defaults={
                    'first_name': user_data[1],
                    'last_name': user_data[2],
                    'password': make_password(user_data[3]),
                }
            )

        for status in statuses_data:
            Status.objects.get_or_create(name=status)

        for label in labels_data:
            Label.objects.get_or_create(name=label)

        for task in tasks_data:
            Task.objects.get_or_create(
                name=task.get('name'),
                description=task.get('description'),
                status=task.get('status'),
                author=task.get('author'),
                executor=task.get('executor'),
            )
            for label in task.get('labels'):
                Label.objects.get_or_create(name=label)
