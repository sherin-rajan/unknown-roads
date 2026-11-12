from rest_framework import serializers

from .models import Review, ReviewPhoto
from apps.packages.models import PackageBooking


class ReviewPhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReviewPhoto
        fields = ["id", "image", "uploaded_at"]
        read_only_fields = ["id", "uploaded_at"]


class ReviewSerializer(serializers.ModelSerializer):

    booking_reference = serializers.UUIDField(
        source="booking.booking_reference",
        read_only=True,
    )

    package_name = serializers.CharField(
        source="booking.package.name",
        read_only=True,
    )

    customer_name = serializers.CharField(
        source="booking.user.username",
        read_only=True,
    )

    photos = ReviewPhotoSerializer(many=True, read_only=True)

    images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False,
    )

    class Meta:
        model = Review
        fields = [
            "id",
            "booking",
            "booking_reference",
            "package_name",
            "customer_name",
            "rating",
            "feedback",
            "status",
            "photos",
            "images",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "status",
            "created_at",
            "updated_at",
        ]

    def validate_booking(self, booking):
        request = self.context["request"]

        if booking.user_id != request.user.id:
            raise serializers.ValidationError(
                "You can review only your own booking."
            )

        if booking.booking_status != "completed":
            raise serializers.ValidationError(
                "You can review only completed bookings."
            )

        if Review.objects.filter(booking=booking).exists():
            raise serializers.ValidationError(
                "You have already submitted a review for this booking."
            )

        return booking

    def create(self, validated_data):
        images = validated_data.pop("images", [])

        review = Review.objects.create(**validated_data)

        for image in images:
            ReviewPhoto.objects.create(
                review=review,
                image=image,
            )

        return review

    def update(self, instance, validated_data):
        images = validated_data.pop("images", [])

        for attribute, value in validated_data.items():
            setattr(instance, attribute, value)

        # Editing an approved review requires fresh admin approval.
        instance.status = "pending"
        instance.save()

        for image in images:
            ReviewPhoto.objects.create(
                review=instance,
                image=image,
            )

        return instance
