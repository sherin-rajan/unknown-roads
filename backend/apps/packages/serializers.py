from rest_framework import serializers

from .models import (
    PackageCategory,
    TravelPackage,
    PackageDay,
    PackageDeparture,
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
