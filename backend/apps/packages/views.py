from rest_framework import generics
from rest_framework.permissions import AllowAny
from accounts.permissions import IsManager
from rest_framework.permissions import IsAuthenticated

from .models import TravelPackage, PackageCategory, PackageDay, PackageDeparture, GroupSize, PackageEnquiry
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
            status="published",
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