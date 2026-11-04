from rest_framework import generics
from rest_framework.permissions import AllowAny
from accounts.permissions import IsManager

from .models import TravelPackage, PackageCategory
from .serializers import (
    PackageCategorySerializer,
    TravelPackageListSerializer,
    TravelPackageDetailSerializer,
    ManagerTravelPackageSerializer
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