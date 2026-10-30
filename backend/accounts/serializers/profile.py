from datetime import date
import re
from django.contrib.auth.models import User
from rest_framework import serializers
from ..models import UserProfile
from apps.destinations.models import Category

class CustomerProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        source="user.username",
        read_only=True
    )

    first_name = serializers.CharField(
        source="user.first_name",
        required=False,
        allow_blank=True,
        max_length=150
    )

    last_name = serializers.CharField(
        source="user.last_name",
        required=False,
        allow_blank=True,
        max_length=150
    )

    email = serializers.EmailField(
        source="user.email",
        required=False,
        allow_blank=False
    )

    preferred_categories = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Category.objects.all(),
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

    def validate_first_name(self, value):
        return value.strip()

    def validate_last_name(self, value):
        return value.strip()

    def validate_email(self, value):
        value = value.strip().lower()

        current_user = self.instance.user

        if User.objects.filter(
            email__iexact=value
        ).exclude(id=current_user.id).exists():
            raise serializers.ValidationError(
                "This email is already used by another account."
            )

        return value

    def validate_phone_number(self, value):
        value = value.strip()

        if value and not re.fullmatch(r"^(?:\+91)?[0-9]{10}$", value):
            raise serializers.ValidationError(
                "Enter a valid 10-digit mobile number. You may include the +91 country code."
            )

        return value

    def validate_date_of_birth(self, value):
        if value and value > date.today():
            raise serializers.ValidationError(
                "Date of birth cannot be in the future."
            )

        return value

    def validate_place(self, value):
        value = value.strip()

        if len(value) > 150:
            raise serializers.ValidationError(
                "Place cannot exceed 150 characters."
            )

        return value

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", {})

        for field, value in user_data.items():
            setattr(instance.user, field, value)

        if user_data:
            instance.user.save()

        return super().update(instance, validated_data)
