from django.conf import settings
from django.db import models


class Notification(models.Model):

    NOTIFICATION_TYPES = [
        ("new_booking", "New Booking"),
        ("booking_confirmed", "Booking Confirmed"),
        ("booking_rejected", "Booking Rejected"),
        ("booking_cancelled", "Booking Cancelled"),
        ("customer_cancelled", "Customer Cancelled Booking"),
        ("booking_expired", "Booking Expired"),
    ]

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    booking = models.ForeignKey(
        "packages.PackageBooking",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="notifications"
    )

    title = models.CharField(max_length=200)
    message = models.TextField()

    notification_type = models.CharField(
        max_length=40,
        choices=NOTIFICATION_TYPES
    )

    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["recipient", "is_read"]),
        ]

    def __str__(self):
        return f"{self.recipient.username} - {self.title}"