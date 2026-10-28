from django.contrib.auth import get_user_model
import resend
from django.conf import settings

from .models import Notification


User = get_user_model()


def create_notification(
    user,
    task,
    message,
    notification_type
):

    return Notification.objects.create(
        user=user,
        task=task,
        message=message,
        notification_type=notification_type,
    )

def send_task_reminder_email(
    user,
    task,
    subject,
    message
):
    """
    Send a task reminder email through Resend.
    """

    if not user.email:
        return None

    resend.api_key = settings.RESEND_API_KEY

    params = {
        "from": settings.RESEND_FROM_EMAIL,
        "to": [user.email],
        "subject": subject,
        "html": f"""
            <div style="
                font-family: Arial, sans-serif;
                max-width: 600px;
                margin: auto;
                padding: 20px;
                line-height: 1.6;
            ">

                <h2>TaskHero Reminder</h2>

                <p>
                    Hello {user.first_name or user.username},
                </p>

                <p>
                    {message}
                </p>

                <hr>

                <p>
                    <strong>Task:</strong> {task.title}
                </p>

                <p>
                    <strong>Due:</strong>
                    {task.due_date.strftime("%B %d, %Y at %H:%M")}
                </p>

                <p>
                    <strong>Priority:</strong>
                    {task.get_priority_display()}
                </p>

                <p>
                    Please log in to TaskHero to view or update your task.
                </p>

                <p>
                    — TaskHero
                </p>

            </div>
        """
    }

    return resend.Emails.send(params)