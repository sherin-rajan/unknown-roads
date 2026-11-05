from rest_framework import serializers

from .models import (
    PackageCategory,
    TravelPackage,
    PackageDay,
    PackageDeparture,
    GroupSize,
    PackageEnquiry
)


class PackageCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageCategory
        fields = ["id", "name", "description"]


class PackageDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageDay
        fields = [
            "id",
            "day_number",
            "title",
            "description",
            "activities",
        ]


class PackageDepartureSerializer(serializers.ModelSerializer):
    group_size_name = serializers.CharField(
        source="group_size.get_name_display",
        read_only=True,
    )

    class Meta:
        model = PackageDeparture
        fields = [
            "id",
            "start_date",
            "end_date",
            "price_per_person",
            "group_size",
            "group_size_name",
            "total_seats",
            "available_seats",
            "availability_status",
        ]


class TravelPackageListSerializer(serializers.ModelSerializer):
    main_destination_name = serializers.CharField(
        source="main_destination.name",
        read_only=True,
    )
    categories = PackageCategorySerializer(many=True, read_only=True)

    class Meta:
        model = TravelPackage
        fields = [
            "id",
            "name",
            "trip_mode",
            "group_type",
            "main_destination",
            "main_destination_name",
            "categories",
            "duration_days",
            "duration_nights",
            "status",
            "publication_status",
            "cover_image",
        ]


class TravelPackageDetailSerializer(TravelPackageListSerializer):
    itinerary = PackageDaySerializer(
        source="itinerary_days",
        many=True,
        read_only=True,
    )
    departures = serializers.SerializerMethodField()

    class Meta(TravelPackageListSerializer.Meta):
        fields = TravelPackageListSerializer.Meta.fields + [
            "itinerary",
            "departures",
        ]

    def get_departures(self, obj):
        departures = obj.departures.all().order_by("start_date")
        return PackageDepartureSerializer(
            departures,
            many=True,
        ).data

class ManagerTravelPackageSerializer(serializers.ModelSerializer):
    categories = PackageCategorySerializer(many=True, read_only=True)

    category_ids = serializers.PrimaryKeyRelatedField(
        queryset=PackageCategory.objects.all(),
        source="categories",
        many=True,
        write_only=True,
        required=False,
    )

    class Meta:
        model = TravelPackage
        fields = [
            "id",
            "name",
            "description",
            "main_destination",
            "categories",
            "category_ids",
            "trip_mode",
            "group_type",
            "duration_days",
            "duration_nights",
            "status",
            "cover_image",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

class ManagerPackageDaySerializer(serializers.ModelSerializer):

    class Meta:
        model = PackageDay
        fields = [
            "id",
            "day_number",
            "title",
            "description",
            "activities",
        ]
        read_only_fields = ["id"]

    def validate_day_number(self, value):
        package = self.context["package"]

        if value > package.duration_days:
            raise serializers.ValidationError(
                f"Day number cannot exceed package duration "
                f"({package.duration_days} days)."
            )

        existing_days = PackageDay.objects.filter(
            package=package,
            day_number=value,
        )

        if self.instance:
            existing_days = existing_days.exclude(pk=self.instance.pk)

        if existing_days.exists():
            raise serializers.ValidationError(
                "An itinerary already exists for this day."
            )

        return value

class ManagerPackageDepartureSerializer(serializers.ModelSerializer):
    group_size_name = serializers.CharField(
        source="group_size.get_name_display",
        read_only=True,
    )

    class Meta:
        model = PackageDeparture
        fields = [
            "id",
            "start_date",
            "end_date",
            "price_per_person",
            "group_size",
            "group_size_name",
            "total_seats",
            "available_seats",
            "availability_status",
        ]
        read_only_fields = [
            "id",
            "total_seats",
            "available_seats",
        ]

    def validate(self, attrs):
        package = self.context["package"]

        start_date = attrs.get(
            "start_date",
            self.instance.start_date if self.instance else None,
        )
        end_date = attrs.get(
            "end_date",
            self.instance.end_date if self.instance else None,
        )

        if start_date and end_date and end_date < start_date:
            raise serializers.ValidationError(
                "End date cannot be earlier than start date."
            )

        group_size = attrs.get(
            "group_size",
            self.instance.group_size if self.instance else None,
        )

        if package.trip_mode == "private" and group_size is not None:
            raise serializers.ValidationError(
                "Private departures cannot have a group size."
            )

        if package.trip_mode == "group" and group_size is None:
            raise serializers.ValidationError(
                "Select a group size for Group departures."
            )

        return attrs

class GroupSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupSize
        fields = ["id", "name", "capacity"]

class PackageEnquiryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageEnquiry
        fields = [
            "id",
            "subject",
            "message",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class ManagerPackageEnquirySerializer(serializers.ModelSerializer):
    customer_username = serializers.CharField(
        source="user.username",
        read_only=True,
    )
    customer_email = serializers.EmailField(
        source="user.email",
        read_only=True,
    )
    package_name = serializers.CharField(
        source="package.name",
        read_only=True,
    )

    class Meta:
        model = PackageEnquiry
        fields = [
            "id",
            "package",
            "package_name",
            "user",
            "customer_username",
            "customer_email",
            "subject",
            "message",
            "status",
            "admin_response",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "package",
            "user",
            "created_at",
            "updated_at",
        ]