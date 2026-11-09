from django.contrib.auth.models import User

from .models import Notification


def create_notification(
    recipient,
    booking,
    title,
    message,
    notification_type
):
    return Notification.objects.create(
        recipient=recipient,
        booking=booking,
        title=title,
        message=message,
        notification_type=notification_type,
    )


def notify_managers(
    booking,
    title,
    message,
    notification_type
):
    managers = User.objects.filter(
        is_active=True,
        profile__role="manager"
    )

    notifications = [
        Notification(
            recipient=manager,
            booking=booking,
            title=title,
            message=message,
            notification_type=notification_type,
        )
        for manager in managers
    ]

    return Notification.objects.bulk_create(notifications)