from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        required=True,
        write_only=True,
        trim_whitespace=False,
        style={"input_type": "password"}
    )

    new_password = serializers.CharField(
        required=True,
        write_only=True,
        trim_whitespace=False,
        validators=[validate_password],
        style={"input_type": "password"}
    )

    confirm_password = serializers.CharField(
        required=True,
        write_only=True,
        trim_whitespace=False,
        style={"input_type": "password"}
    )

    def validate(self, attrs):
        if not attrs["old_password"]:
            raise serializers.ValidationError({
                "old_password": "Current password is required."
            })

        if not attrs["new_password"]:
            raise serializers.ValidationError({
                "new_password": "New password is required."
            })

        if attrs["new_password"] != attrs["confirm_password"]:
            raise serializers.ValidationError({
                "confirm_password": "The passwords do not match."
            })

        if attrs["old_password"] == attrs["new_password"]:
            raise serializers.ValidationError({
                "new_password": (
                    "Choose a password different from your current password."
                )
            })

        return attrs
