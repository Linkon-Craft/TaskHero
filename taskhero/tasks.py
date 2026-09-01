from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from .models import Task, Notification
from .services import create_notification


@shared_task
def send_reminders():

    now = timezone.now()

    upcoming_tasks = Task.objects.filter(
        status__in=["TD", "IN_PRGRS"]
    )

    for task in upcoming_tasks:

        time_until_due = task.due_date - now

        # 24-hour reminder
        if timedelta(hours=23) <= time_until_due <= timedelta(hours=24):

            already_sent = Notification.objects.filter(
                task=task,
                notification_type="DUE_SOON"
            ).exists()

            if not already_sent:

                create_notification(
                    task.added_by,
                    task,
                    "Your task is due within 24 hours.",
                    "DUE_SOON"
                )

        # Overdue reminder
        elif time_until_due.total_seconds() < 0:

            already_sent = Notification.objects.filter(
                task=task,
                notification_type="OVERDUE"
            ).exists()

            if not already_sent:

                create_notification(
                    task.added_by,
                    task,
                    f'Your task "{task.title}" is overdue.',
                    "OVERDUE"
                )