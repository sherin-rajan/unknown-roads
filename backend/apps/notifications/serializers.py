from rest_framework import serializers

from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):

    booking_reference = serializers.UUIDField(
        source="booking.booking_reference",
        read_only=True
    )

    package_name = serializers.CharField(
        source="booking.package.name",
        read_only=True
    )

    class Meta:
        model = Notification
        fields = [
            "id",
            "title",
            "message",
            "notification_type",
            "booking",
            "booking_reference",
            "package_name",
            "is_read",
            "created_at",
        ]
        read_only_fields = fields