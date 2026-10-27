from django.contrib.auth.models import User
from rest_framework import serializers
from ..models import UserProfile

class CustomerProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        source="user.username",
        read_only=True
    )
    first_name = serializers.CharField(
        source="user.first_name",
        required=False
    )
    last_name = serializers.CharField(
        source="user.last_name",
        required=False
    )
    email = serializers.EmailField(
        source="user.email",
        required=False
    )
    preferred_categories = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=__import__(
            "apps.destinations.models",
            fromlist=["Category"]
        ).Category.objects.all(),
        required=False
    )

    class Meta:
        model = UserProfile
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "date_of_birth",
            "place",
            "preferred_categories",
        ]

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", {})

        for field, value in user_data.items():
            setattr(instance.user, field, value)

        if user_data:
            instance.user.save()

        return super().update(instance, validated_data)
