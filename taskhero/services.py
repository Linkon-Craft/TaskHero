from django.contrib.auth import get_user_model

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