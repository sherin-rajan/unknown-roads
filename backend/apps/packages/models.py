from decimal import Decimal
import uuid

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.utils import timezone

from apps.destinations.models import Destination


class PackageCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class TravelPackage(models.Model):

    TRIP_MODE_CHOICES = [
        ("private", "Private"),
        ("group", "Group"),
    ]

    GROUP_TYPE_CHOICES = [
        ("student_group", "Student Group"),
        ("open_group", "Open Group"),
    ]

    STATUS_CHOICES = [
        ("upcoming", "Upcoming"),
        ("scheduled", "Scheduled"),
        ("closed", "Closed"),
    ]

    PUBLICATION_STATUS_CHOICES = [
        ("draft", "Draft"),
        ("published", "Published"),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()

    main_destination = models.ForeignKey(
        Destination,
        on_delete=models.PROTECT,
        related_name="travel_packages"
    )

    categories = models.ManyToManyField(
        PackageCategory,
        related_name="packages",
        blank=True
    )

    trip_mode = models.CharField(
        max_length=20,
        choices=TRIP_MODE_CHOICES
    )

    group_type = models.CharField(
        max_length=20,
        choices=GROUP_TYPE_CHOICES,
        blank=True
    )

    # Kept temporarily to preserve existing package records.
    # New bookings will select their traveller type at booking time.
    traveller_type = models.CharField(
        max_length=20,
        choices=[
            ("solo", "Solo"),
            ("couple", "Couple"),
            ("family", "Family"),
        ],
        blank=True,
        default=""
    )

    duration_days = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    duration_nights = models.PositiveIntegerField(
        validators=[MinValueValidator(0)]
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="upcoming"
    )

    publication_status = models.CharField(
        max_length=20,
        choices=PUBLICATION_STATUS_CHOICES,
        default="draft"
    )

    cover_image = models.ImageField(
        upload_to="packages/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def clean(self):
        super().clean()

        if self.trip_mode == "private" and self.group_type:
            raise ValidationError({
                "group_type": "Private packages cannot have a group type."
            })

        if self.trip_mode == "group" and not self.group_type:
            raise ValidationError({
                "group_type": "Please select Student Group or Open Group."
            })

        if (
            self.duration_days is not None
            and self.duration_nights is not None
            and self.duration_nights >= self.duration_days
        ):
            raise ValidationError({
                "duration_nights": "Nights must be fewer than days."
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class GroupSize(models.Model):
    SIZE_CHOICES = [
        ("small", "Small"),
        ("medium", "Medium"),
        ("large", "Large"),
    ]

    name = models.CharField(
        max_length=20,
        choices=SIZE_CHOICES,
        unique=True
    )

    capacity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    class Meta:
        ordering = ["capacity"]

    def __str__(self):
        return f"{self.get_name_display()} - {self.capacity} seats"


class PackageDay(models.Model):
    package = models.ForeignKey(
        TravelPackage,
        on_delete=models.CASCADE,
        related_name="itinerary_days"
    )

    day_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    activities = models.TextField(blank=True)

    class Meta:
        ordering = ["day_number"]
        constraints = [
            models.UniqueConstraint(
                fields=["package", "day_number"],
                name="unique_package_day"
            )
        ]

    def clean(self):
        super().clean()

        if (
            self.package_id
            and self.day_number
            and self.day_number > self.package.duration_days
        ):
            raise ValidationError({
                "day_number": "Day number cannot exceed package duration."
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.package.name} - Day {self.day_number}"


class PackageDeparture(models.Model):

    AVAILABILITY_CHOICES = [
        ("available", "Available"),
        ("full", "Fully Booked"),
        ("cancelled", "Cancelled"),
    ]

    package = models.ForeignKey(
        TravelPackage,
        on_delete=models.CASCADE,
        related_name="departures"
    )

    start_date = models.DateField()
    end_date = models.DateField()

    price_per_person = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))]
    )

    # Used only for Group departures.
    group_size = models.ForeignKey(
        GroupSize,
        on_delete=models.PROTECT,
        related_name="departures",
        blank=True,
        null=True
    )

    # Capacity is copied from GroupSize when the departure is created.
    # Existing departures keep their original capacity if settings change.
    total_seats = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    available_seats = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    availability_status = models.CharField(
        max_length=20,
        choices=AVAILABILITY_CHOICES,
        default="available"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["start_date"]
        constraints = [
            models.UniqueConstraint(
                fields=["package", "start_date"],
                name="unique_package_departure_date"
            )
        ]

    def clean(self):
        super().clean()

        if self.end_date and self.start_date and self.end_date < self.start_date:
            raise ValidationError({
                "end_date": "End date cannot be earlier than start date."
            })

        if self.package_id:
            if self.package.trip_mode == "private":
                if self.group_size_id or self.total_seats is not None or self.available_seats is not None:
                    raise ValidationError(
                        "Private departures must not have shared seat capacity."
                    )

            elif self.package.trip_mode == "group":
                if not self.group_size_id:
                    raise ValidationError({
                        "group_size": "Select a group size for Group departures."
                    })

                if self.total_seats is None or self.available_seats is None:
                    raise ValidationError(
                        "Group departures must have total and available seats."
                    )

                if self.available_seats > self.total_seats:
                    raise ValidationError({
                        "available_seats": "Available seats cannot exceed total seats."
                    })

                if self.availability_status == "full" and self.available_seats != 0:
                    raise ValidationError({
                        "availability_status": "A fully booked departure must have zero available seats."
                    })

                if self.available_seats == 0 and self.availability_status == "available":
                    raise ValidationError({
                        "availability_status": "Mark this departure as fully booked."
                    })

    def save(self, *args, **kwargs):
        if (
            not self.pk
            and self.package_id
            and self.package.trip_mode == "group"
            and self.group_size_id
        ):
            self.total_seats = self.group_size.capacity
            self.available_seats = self.group_size.capacity

        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.package.name} - {self.start_date}"


class PackageEnquiry(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("responded", "Responded"),
        ("closed", "Closed"),
    ]

    package = models.ForeignKey(
        TravelPackage,
        on_delete=models.PROTECT,
        related_name="enquiries"
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="package_enquiries"
    )

    subject = models.CharField(max_length=200)
    message = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    admin_response = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.package.name}"


class PackageBooking(models.Model):

    TRAVELLER_TYPE_CHOICES = [
        ("solo", "Solo"),
        ("couple", "Couple"),
        ("family", "Family"),
    ]

    BOOKING_STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("rejected", "Rejected"),
        ("cancelled", "Cancelled"),
        ("completed", "Completed"),
        ("expired", "Expired"),
    ]

    booking_reference = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )

    package = models.ForeignKey(
        TravelPackage,
        on_delete=models.PROTECT,
        related_name="bookings"
    )

    departure = models.ForeignKey(
        PackageDeparture,
        on_delete=models.PROTECT,
        related_name="bookings"
    )

    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="package_bookings"
    )

    # Only used for Private bookings.
    traveller_type = models.CharField(
        max_length=20,
        choices=TRAVELLER_TYPE_CHOICES,
        blank=True
    )

    number_of_travellers = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    price_per_person = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))]
    )

    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    booking_status = models.CharField(
        max_length=20,
        choices=BOOKING_STATUS_CHOICES,
        default="pending"
    )

    # Used to release Group seats if a pending booking expires.
    reservation_expires_at = models.DateTimeField(
        blank=True,
        null=True
    )

    booked_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-booked_at"]

    def clean(self):
        super().clean()

        if self.package_id and self.departure_id:
            if self.departure.package_id != self.package_id:
                raise ValidationError({
                    "departure": "This departure does not belong to the selected package."
                })

            if self.package.trip_mode == "private":
                if not self.traveller_type:
                    raise ValidationError({
                        "traveller_type": "Select Solo, Couple or Family."
                    })

                if self.traveller_type == "solo" and self.number_of_travellers != 1:
                    raise ValidationError({
                        "number_of_travellers": "Solo bookings require one traveller."
                    })

                if self.traveller_type == "couple" and self.number_of_travellers != 2:
                    raise ValidationError({
                        "number_of_travellers": "Couple bookings require two travellers."
                    })

                if self.traveller_type == "family" and not 3 <= self.number_of_travellers <= 5:
                    raise ValidationError({
                        "number_of_travellers": "Family bookings allow 3 to 5 travellers."
                    })

            elif self.package.trip_mode == "group" and self.traveller_type:
                raise ValidationError({
                    "traveller_type": "Traveller type is only used for Private bookings."
                })

        if (
            self.price_per_person is not None
            and self.number_of_travellers is not None
            and self.total_amount is not None
        ):
            expected_total = self.price_per_person * self.number_of_travellers

            if self.total_amount != expected_total:
                raise ValidationError({
                    "total_amount": "Total must equal price per person multiplied by travellers."
                })

    def save(self, *args, **kwargs):
        if self.price_per_person is not None and self.number_of_travellers:
            self.total_amount = self.price_per_person * self.number_of_travellers

        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking {self.booking_reference}"


class BookingTraveller(models.Model):

    booking = models.ForeignKey(
        PackageBooking,
        on_delete=models.CASCADE,
        related_name="travellers"
    )

    full_name = models.CharField(max_length=200)
    age = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.full_name} - {self.booking.booking_reference}"


class BookingStatusHistory(models.Model):

    booking = models.ForeignKey(
        PackageBooking,
        on_delete=models.CASCADE,
        related_name="status_history"
    )

    old_status = models.CharField(max_length=20, blank=True)
    new_status = models.CharField(max_length=20)

    changed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="booking_status_changes"
    )

    note = models.TextField(blank=True)
    changed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-changed_at"]

    def __str__(self):
        return f"{self.booking.booking_reference}: {self.new_status}"