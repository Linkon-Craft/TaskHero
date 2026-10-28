from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from .models import Task, Notification
from .services import (
    create_notification,
    send_task_reminder_email,
)


@shared_task
def send_reminders():

    now = timezone.now()

    upcoming_tasks = Task.objects.filter(
        status__in=["TD", "IN_PRGRS"]
    )

    for task in upcoming_tasks:

        time_until_due = task.due_date - now

        # -----------------------------------
        # DUE SOON
        # -----------------------------------

        if timedelta(hours=23) <= time_until_due <= timedelta(hours=24):

            already_sent = Notification.objects.filter(
                task=task,
                user=task.added_by,
                notification_type=Notification.NotificationType.DUE_SOON
            ).exists()

            if not already_sent:

                message = (
                    f'Your task "{task.title}" '
                    f'is due within 24 hours.'
                )

                # Create database notification
                create_notification(
                    task.added_by,
                    task,
                    message,
                    Notification.NotificationType.DUE_SOON
                )

                # Send email
                try:

                    send_task_reminder_email(
                        user=task.added_by,
                        task=task,
                        subject=(
                            f"TaskHero Reminder: "
                            f"{task.title} is due soon"
                        ),
                        message=message
                    )

                except Exception as e:

                    print(
                        f"Failed to send email for task "
                        f"{task.id}: {e}"
                    )

        # -----------------------------------
        # OVERDUE
        # -----------------------------------

        elif time_until_due.total_seconds() < 0:

            already_sent = Notification.objects.filter(
                task=task,
                user=task.added_by,
                notification_type=Notification.NotificationType.OVERDUE
            ).exists()

            if not already_sent:

                message = (
                    f'Your task "{task.title}" is overdue.'
                )

                # Create database notification
                create_notification(
                    task.added_by,
                    task,
                    message,
                    Notification.NotificationType.OVERDUE
                )

                # Send email
                try:

                    send_task_reminder_email(
                        user=task.added_by,
                        task=task,
                        subject=(
                            f"TaskHero: "
                            f"{task.title} is overdue"
                        ),
                        message=message
                    )

                except Exception as e:

                    print(
                        f"Failed to send email for task "
                        f"{task.id}: {e}"
                    )


                    