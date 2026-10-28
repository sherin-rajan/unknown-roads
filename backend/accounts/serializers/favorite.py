from rest_framework import serializers
from apps.destinations.models import Favorite, Destination

class FavoriteSerializer(serializers.ModelSerializer):
    destination = serializers.PrimaryKeyRelatedField(
        queryset=Destination.objects.all()
    )

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

    destination_image = serializers.ImageField(
        source="destination.image",
        read_only=True
    )

    class Meta:
        model = Favorite
        fields = [
            "id",
            "destination",
            "destination_name",
            "destination_state",
            "destination_location",
            "destination_image",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]
