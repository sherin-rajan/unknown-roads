from rest_framework import generics
from rest_framework.permissions import AllowAny
from accounts.permissions import IsManager
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from rest_framework.response import Response
from rest_framework import status

from .models import (TravelPackage, 
                     PackageCategory, 
                     PackageDay, 
                     PackageDeparture, 
                     GroupSize, 
                     PackageEnquiry, 
                     PackageBooking,
                     BookingStatusHistory)
from .serializers import (
    PackageCategorySerializer,
    TravelPackageListSerializer,
    TravelPackageDetailSerializer,
    ManagerTravelPackageSerializer,
    ManagerPackageDaySerializer,
    ManagerPackageDepartureSerializer,
    GroupSizeSerializer,
    PackageEnquiryCreateSerializer,
    ManagerPackageEnquirySerializer,
    CustomerPackageEnquirySerializer,
    CustomerPackageBookingSerializer,
    CustomerPackageBookingListSerializer,
    ManagerPackageBookingSerializer,
    ManagerPackageBookingStatusSerializer,
    CustomerPackageBookingCancelSerializer
)


class PackageCategoryListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = PackageCategorySerializer
    queryset = PackageCategory.objects.all().order_by("name")


class PublishedPackageListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = TravelPackageListSerializer

    def get_queryset(self):
        return (
            TravelPackage.objects
            .filter(publication_status="published")
            .select_related("main_destination")
            .prefetch_related("categories")
            .order_by("-created_at")
        )


class PublishedPackageDetailView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = TravelPackageDetailSerializer

    def get_queryset(self):
        return (
            TravelPackage.objects
            .filter(publication_status="published")
            .select_related("main_destination")
            .prefetch_related(
                "categories",
                "itinerary_days",
                "departures",
            )
        )

class ManagerPackageListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsManager]
    serializer_class = ManagerTravelPackageSerializer

    def get_queryset(self):
        return (
            TravelPackage.objects
            .select_related("main_destination")
            .prefetch_related("categories")
            .order_by("-created_at")
        )


class ManagerPackageDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsManager]
    serializer_class = ManagerTravelPackageSerializer

    queryset = TravelPackage.objects.all()

class ManagerPackageItineraryListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsManager]
    serializer_class = ManagerPackageDaySerializer

    def get_package(self):
        return generics.get_object_or_404(
            TravelPackage,
            pk=self.kwargs["package_id"],
        )

    def get_queryset(self):
        return PackageDay.objects.filter(
            package=self.get_package()
        ).order_by("day_number")

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["package"] = self.get_package()
        return context

    def perform_create(self, serializer):
        serializer.save(package=self.get_package())


class ManagerPackageItineraryDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsManager]
    serializer_class = ManagerPackageDaySerializer
    lookup_url_kwarg = "day_id"

    def get_package(self):
        return generics.get_object_or_404(
            TravelPackage,
            pk=self.kwargs["package_id"],
        )

    def get_queryset(self):
        return PackageDay.objects.filter(
            package=self.get_package()
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["package"] = self.get_package()
        return context

class ManagerPackageDepartureListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsManager]
    serializer_class = ManagerPackageDepartureSerializer

    def get_package(self):
        return generics.get_object_or_404(
            TravelPackage,
            pk=self.kwargs["package_id"],
        )

    def get_queryset(self):
        return PackageDeparture.objects.filter(
            package=self.get_package()
        ).order_by("start_date")

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["package"] = self.get_package()
        return context

    def perform_create(self, serializer):
        serializer.save(package=self.get_package())


class ManagerPackageDepartureDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsManager]
    serializer_class = ManagerPackageDepartureSerializer
    lookup_url_kwarg = "departure_id"

    def get_package(self):
        return generics.get_object_or_404(
            TravelPackage,
            pk=self.kwargs["package_id"],
        )

    def get_queryset(self):
        return PackageDeparture.objects.filter(
            package=self.get_package()
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["package"] = self.get_package()
        return context

class GroupSizeListView(generics.ListAPIView):
    queryset = GroupSize.objects.all().order_by("capacity")
    serializer_class = GroupSizeSerializer
    permission_classes = [IsManager]

class CustomerPackageEnquiryCreateView(generics.CreateAPIView):
    serializer_class = PackageEnquiryCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_package(self):
        return generics.get_object_or_404(
            TravelPackage,
            pk=self.kwargs["package_id"],
            status="scheduled",
        )

    def perform_create(self, serializer):
        serializer.save(
            package=self.get_package(),
            user=self.request.user,
        )


class ManagerPackageEnquiryListView(generics.ListAPIView):
    serializer_class = ManagerPackageEnquirySerializer
    permission_classes = [IsManager]

    def get_queryset(self):
        return PackageEnquiry.objects.select_related(
            "package", "user"
        ).order_by("-created_at")


class ManagerPackageEnquiryDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = ManagerPackageEnquirySerializer
    permission_classes = [IsManager]

    def get_queryset(self):
        return PackageEnquiry.objects.select_related(
            "package", "user"
        )

class CustomerPackageEnquiryListView(generics.ListAPIView):
    serializer_class = CustomerPackageEnquirySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PackageEnquiry.objects.filter(
            user=self.request.user
        ).select_related(
            "package"
        ).order_by("-created_at")

class CustomerPackageBookingCreateView(generics.CreateAPIView):
    serializer_class = CustomerPackageBookingSerializer
    permission_classes = [IsAuthenticated]

class CustomerPackageBookingListView(generics.ListAPIView):
    serializer_class = CustomerPackageBookingListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            PackageBooking.objects
            .filter(user=self.request.user)
            .select_related("package", "departure")
            .prefetch_related("travellers")
            .order_by("-booked_at")
        )

class CustomerPackageBookingDetailView(generics.RetrieveAPIView):
    serializer_class = CustomerPackageBookingListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            PackageBooking.objects
            .filter(user=self.request.user)
            .select_related("package", "departure")
            .prefetch_related("travellers")
        )

class ManagerPackageBookingListView(generics.ListAPIView):
    serializer_class = ManagerPackageBookingSerializer
    permission_classes = [IsManager]

    def get_queryset(self):
        return (
            PackageBooking.objects
            .select_related("package", "departure", "user")
            .prefetch_related("travellers", "status_history")
            .order_by("-booked_at")
        ) 

class ManagerPackageBookingDetailView(generics.RetrieveAPIView):
    serializer_class = ManagerPackageBookingSerializer
    permission_classes = [IsManager]

    def get_queryset(self):
        return (
            PackageBooking.objects
            .select_related("package", "departure", "user")
            .prefetch_related("travellers", "status_history")
        ) 

class ManagerPackageBookingStatusUpdateView(generics.UpdateAPIView):
    serializer_class = ManagerPackageBookingStatusSerializer
    permission_classes = [IsManager]
    http_method_names = ["patch", "options", "head"]

    def get_queryset(self):
        return (
            PackageBooking.objects
            .select_related("package", "departure", "user")
            .select_for_update()
        )

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def perform_update(self, serializer):
        booking = serializer.instance

        old_status = booking.booking_status
        new_status = serializer.validated_data["booking_status"]

        serializer.save()

        # Release reserved seats for rejected or cancelled group bookings.
        if (
            booking.package.trip_mode == "group"
            and new_status in ["rejected", "cancelled"]
        ):
            departure = PackageDeparture.objects.select_for_update().get(
                pk=booking.departure_id
            )

            if departure.availability_status != "cancelled":
                departure.available_seats = min(
                    departure.total_seats,
                    departure.available_seats + booking.number_of_travellers
                )

                departure.availability_status = (
                    "available" if departure.available_seats > 0 else "full"
                )

                departure.save()

        # Record the status change.
        BookingStatusHistory.objects.create(
            booking=booking,
            old_status=old_status,
            new_status=new_status,
            changed_by=self.request.user,
            note="Booking status updated by manager."
        )

class CustomerPackageBookingCancelView(generics.GenericAPIView):
    serializer_class = CustomerPackageBookingCancelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PackageBooking.objects.filter(
            user=self.request.user
        ).select_related("package", "departure")

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        booking = self.get_object()

        context = self.get_serializer_context()
        context["booking"] = booking

        serializer = self.get_serializer(
            data=request.data,
            context=context
        )
        serializer.is_valid(raise_exception=True)

        old_status = booking.booking_status

        booking.booking_status = "cancelled"
        booking.save()

        # Release reserved group seats.
        if booking.package.trip_mode == "group":
            departure = PackageDeparture.objects.select_for_update().get(
                pk=booking.departure_id
            )

            if departure.availability_status != "cancelled":
                departure.available_seats = min(
                    departure.total_seats,
                    departure.available_seats + booking.number_of_travellers
                )

                departure.availability_status = (
                    "available" if departure.available_seats > 0 else "full"
                )

                departure.save()

        # Record cancellation history.
        BookingStatusHistory.objects.create(
            booking=booking,
            old_status=old_status,
            new_status="cancelled",
            changed_by=request.user,
            note="Booking cancelled by customer."
        )

        return Response(
            {
                "message": "Booking cancelled successfully.",
                "booking_reference": str(booking.booking_reference),
                "booking_status": booking.booking_status,
            },
            status=status.HTTP_200_OK
        )