
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from apps.packages.models import (
    PackageBooking,
    PackageDeparture,
    BookingStatusHistory,
)


class Command(BaseCommand):
    help = "Expire overdue pending group bookings and release reserved seats."

    def handle(self, *args, **options):
        now = timezone.now()

        expired_booking_ids = list(
            PackageBooking.objects.filter(
                booking_status="pending",
                package__trip_mode="group",
                reservation_expires_at__isnull=False,
                reservation_expires_at__lte=now,
            ).values_list("id", flat=True)
        )

        expired_count = 0

        for booking_id in expired_booking_ids:
            with transaction.atomic():
                try:
                    booking = (
                        PackageBooking.objects
                        .select_for_update()
                        .select_related("package")
                        .get(pk=booking_id)
                    )
                except PackageBooking.DoesNotExist:
                    continue

                # Recheck because another request may have changed it.
                if (
                    booking.booking_status != "pending"
                    or booking.package.trip_mode != "group"
                    or booking.reservation_expires_at is None
                    or booking.reservation_expires_at > timezone.now()
                ):
                    continue

                departure = (
                    PackageDeparture.objects
                    .select_for_update()
                    .get(pk=booking.departure_id)
                )

                old_status = booking.booking_status
                booking.booking_status = "expired"
                booking.save(update_fields=["booking_status", "updated_at"])

                # Release seats unless the departure itself was cancelled.
                if departure.availability_status != "cancelled":
                    departure.available_seats = min(
                        departure.total_seats,
                        departure.available_seats
                        + booking.number_of_travellers,
                    )

                    departure.availability_status = (
                        "available"
                        if departure.available_seats > 0
                        else "full"
                    )

                    departure.save(
                        update_fields=[
                            "available_seats",
                            "availability_status",
                        ]
                    )

                BookingStatusHistory.objects.create(
                    booking=booking,
                    old_status=old_status,
                    new_status="expired",
                    changed_by=None,
                    note="Booking automatically expired after the reservation period.",
                )

                expired_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Booking expiry completed. {expired_count} booking(s) expired."
            )
        )
