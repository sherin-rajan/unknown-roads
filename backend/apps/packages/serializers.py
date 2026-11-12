from rest_framework import serializers
from datetime import timedelta
from django.db import transaction
from django.utils import timezone
from apps.notifications.services import notify_managers

from .models import (
    PackageCategory,
    TravelPackage,
    PackageDay,
    PackageDeparture,
    GroupSize,
    PackageEnquiry,
    PackageBooking,
    BookingTraveller,
    BookingStatusHistory,
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
            "description",
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
            "cancellation_days_before",
            "main_destination",
            "categories",
            "category_ids",
            "trip_mode",
            "group_type",
            "duration_days",
            "duration_nights",
            "status",
            "publication_status",
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

class CustomerPackageEnquirySerializer(serializers.ModelSerializer):
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
            "subject",
            "message",
            "status",
            "admin_response",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields

class BookingTravellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingTraveller
        fields = ["full_name", "age"]
        extra_kwargs = {
            "age": {"required": False, "allow_null": True}
        }


class CustomerPackageBookingSerializer(serializers.ModelSerializer):
    travellers = BookingTravellerSerializer(many=True)

    departure = serializers.PrimaryKeyRelatedField(
        queryset=PackageDeparture.objects.select_related("package").all()
    )

    class Meta:
        model = PackageBooking
        fields = [
            "id",
            "booking_reference",
            "package",
            "departure",
            "traveller_type",
            "number_of_travellers",
            "travellers",
            "price_per_person",
            "total_amount",
            "booking_status",
            "reservation_expires_at",
            "booked_at",
        ]

        read_only_fields = [
            "id",
            "booking_reference",
            "package",
            "price_per_person",
            "total_amount",
            "booking_status",
            "reservation_expires_at",
            "booked_at",
        ]

    def validate(self, attrs):
        departure = attrs["departure"]
        package = departure.package

        number = attrs["number_of_travellers"]
        traveller_type = attrs.get("traveller_type", "")
        travellers = attrs["travellers"]

        if package.status != "scheduled":
            raise serializers.ValidationError(
                "This package is not available for booking."
            )

        if departure.start_date <= timezone.localdate():
            raise serializers.ValidationError(
                "This departure date is no longer available."
            )

        if departure.availability_status != "available":
            raise serializers.ValidationError(
                "This departure is not available."
            )

        if len(travellers) != number:
            raise serializers.ValidationError(
                "Traveller details must match the number of travellers."
            )

        if package.trip_mode == "private":
            valid_types = {
                "solo": 1,
                "couple": 2,
            }

            if traveller_type == "family":
                if not 3 <= number <= 5:
                    raise serializers.ValidationError(
                        "Family bookings allow 3 to 5 travellers."
                    )
            elif traveller_type in valid_types:
                if number != valid_types[traveller_type]:
                    raise serializers.ValidationError(
                        "Traveller count does not match traveller type."
                    )
            else:
                raise serializers.ValidationError(
                    "Select Solo, Couple or Family."
                )

        elif package.trip_mode == "group" and traveller_type:
            raise serializers.ValidationError(
                "Traveller type is not required for Group bookings."
            )

        return attrs

    def create(self, validated_data):
        travellers_data = validated_data.pop("travellers")
        departure = validated_data.pop("departure")

        with transaction.atomic():

            departure = PackageDeparture.objects.select_for_update().select_related(
                "package"
            ).get(pk=departure.pk)

            package = departure.package
            number = validated_data["number_of_travellers"]

            if package.status != "scheduled":
                raise serializers.ValidationError(
                    "This package is not available for booking."
                )

            if departure.start_date <= timezone.localdate():
                raise serializers.ValidationError(
                    "This departure date is no longer available."
                )

            if departure.availability_status != "available":
                raise serializers.ValidationError(
                    "This departure is not available."
                )

            if package.trip_mode == "group":
                if departure.available_seats is None:
                    raise serializers.ValidationError(
                        "Group departure capacity is not configured."
                    )

                if departure.available_seats < number:
                    raise serializers.ValidationError(
                        "Not enough seats are available."
                    )

            price = departure.price_per_person
            total = price * number

            expires_at = None

            if package.trip_mode == "group":
                expires_at = timezone.now() + timedelta(hours=24)

            booking = PackageBooking.objects.create(
                package=package,
                departure=departure,
                user=self.context["request"].user,
                traveller_type=validated_data.get("traveller_type", ""),
                number_of_travellers=number,
                price_per_person=price,
                total_amount=total,
                reservation_expires_at=expires_at,
            )

            BookingTraveller.objects.bulk_create([
                BookingTraveller(
                    booking=booking,
                    **traveller
                )
                for traveller in travellers_data
            ])

            BookingStatusHistory.objects.create(
                booking=booking,
                old_status="",
                new_status="pending",
                changed_by=self.context["request"].user,
                note="Booking submitted by customer.",
            )

            if package.trip_mode == "group":
                departure.available_seats -= number

                if departure.available_seats == 0:
                    departure.availability_status = "full"

                departure.save()

            notify_managers(
                booking=booking,
                title="New package booking",
                message=(
                    f"{booking.user.username} submitted a booking "
                    f"for {package.name}."
                ),
                notification_type="new_booking",
            )

            return booking

class CustomerPackageBookingListSerializer(serializers.ModelSerializer):
    package_name = serializers.CharField(
        source="package.name",
        read_only=True
    )

    departure_start_date = serializers.DateField(
        source="departure.start_date",
        read_only=True
    )

    departure_end_date = serializers.DateField(
        source="departure.end_date",
        read_only=True
    )

    travellers = BookingTravellerSerializer(
        many=True,
        read_only=True
    )

    cancellation_deadline = serializers.SerializerMethodField()
    can_cancel = serializers.SerializerMethodField()

    class Meta:
        model = PackageBooking
        fields = [
            "id",
            "booking_reference",
            "package",
            "package_name",
            "departure",
            "departure_start_date",
            "departure_end_date",
            "traveller_type",
            "number_of_travellers",
            "travellers",
            "price_per_person",
            "total_amount",
            "booking_status",
            "cancellation_deadline",
            "can_cancel",
            "reservation_expires_at",
            "booked_at",
            "updated_at",
        ]
        read_only_fields = fields

    def get_cancellation_deadline(self, obj):
        return (
            obj.departure.start_date
            - timedelta(days=obj.package.cancellation_days_before)
        )


    def get_can_cancel(self, obj):
        allowed_statuses = ["pending", "confirmed"]

        cancellation_deadline = (
            obj.departure.start_date
            - timedelta(days=obj.package.cancellation_days_before)
        )

        return (
            obj.booking_status in allowed_statuses
            and timezone.localdate() <= cancellation_deadline
        )


class BookingStatusHistorySerializer(serializers.ModelSerializer):
    changed_by_username = serializers.CharField(
        source="changed_by.username",
        read_only=True
    )

    class Meta:
        model = BookingStatusHistory
        fields = [
            "id",
            "old_status",
            "new_status",
            "changed_by",
            "changed_by_username",
            "note",
            "changed_at",
        ]


class ManagerPackageBookingSerializer(serializers.ModelSerializer):
    package_name = serializers.CharField(
        source="package.name",
        read_only=True
    )

    customer_username = serializers.CharField(
        source="user.username",
        read_only=True
    )

    customer_email = serializers.EmailField(
        source="user.email",
        read_only=True
    )

    departure_start_date = serializers.DateField(
        source="departure.start_date",
        read_only=True
    )

    departure_end_date = serializers.DateField(
        source="departure.end_date",
        read_only=True
    )

    travellers = BookingTravellerSerializer(
        many=True,
        read_only=True
    )

    status_history = BookingStatusHistorySerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = PackageBooking
        fields = [
            "id",
            "booking_reference",
            "package",
            "package_name",
            "departure",
            "departure_start_date",
            "departure_end_date",
            "user",
            "customer_username",
            "customer_email",
            "traveller_type",
            "number_of_travellers",
            "travellers",
            "price_per_person",
            "total_amount",
            "booking_status",
            "reservation_expires_at",
            "booked_at",
            "updated_at",
            "status_history",
        ]
        read_only_fields = fields

class ManagerPackageBookingStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageBooking
        fields = ["booking_status"]

    def validate_booking_status(self, value):
        current_status = self.instance.booking_status

        allowed_transitions = {
            "pending": ["confirmed", "rejected", "cancelled"],
            "confirmed": ["cancelled", "completed"],
        }

        if value not in allowed_transitions.get(current_status, []):
            raise serializers.ValidationError(
                f"Cannot change booking status from "
                f"{current_status} to {value}."
            )

        return value

class CustomerPackageBookingCancelSerializer(serializers.Serializer):

    def validate(self, attrs):
        booking = self.context["booking"]

        allowed_statuses = ["pending", "confirmed"]

        if booking.booking_status not in allowed_statuses:
            raise serializers.ValidationError(
                "Only pending or confirmed bookings can be cancelled."
            )

        cancellation_deadline = (
            booking.departure.start_date
            - timedelta(days=booking.package.cancellation_days_before)
        )

        if timezone.localdate() > cancellation_deadline:
            raise serializers.ValidationError(
                f"This booking can only be cancelled up to "
                f"{booking.package.cancellation_days_before} days "
                f"before departure. The cancellation deadline "
                f"was {cancellation_deadline}."
            )

        return attrs
