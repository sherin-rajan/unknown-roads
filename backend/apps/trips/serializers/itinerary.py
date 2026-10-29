from rest_framework import serializers
from apps.destinations.models import Destination
from apps.trips.models import TripDestination


class TripDestinationSerializer(serializers.ModelSerializer):
    destination_name = serializers.CharField(
        source="destination.name",
        read_only=True
    )
    destination_state = serializers.CharField(
        source="destination.state",
        read_only=True
    )
    destination_location = serializers.CharField(
        source="destination.location",
        read_only=True
    )

    destination = serializers.PrimaryKeyRelatedField(
        queryset=Destination.objects.all()
    )

    class Meta:
        model = TripDestination
        fields = [
            "id",
            "destination",
            "destination_name",
            "destination_state",
            "destination_location",
            "visit_date",
            "notes",
            "order",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def validate(self, attrs):
        trip = (
            self.instance.trip
            if self.instance
            else self.context.get("trip")
        )

        visit_date = attrs.get(
            "visit_date",
            getattr(self.instance, "visit_date", None)
        )

        if trip and visit_date:
            if visit_date < trip.start_date or visit_date > trip.end_date:
                raise serializers.ValidationError({
                    "visit_date": (
                        "Visit date must fall within the trip's start "
                        "and end dates."
                    )
                })

        return attrs
