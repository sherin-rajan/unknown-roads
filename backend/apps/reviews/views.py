from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from accounts.permissions import IsCustomer, IsManager

from .models import Review
from .serializers import ReviewSerializer


class CustomerReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsCustomer]

    def get_queryset(self):
        return (
            Review.objects
            .filter(booking__user=self.request.user)
            .select_related("booking", "booking__package", "booking__user")
            .prefetch_related("photos")
        )

    def perform_create(self, serializer):
        serializer.save()


class CustomerReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsCustomer]

    def get_queryset(self):
        return (
            Review.objects
            .filter(booking__user=self.request.user)
            .select_related("booking", "booking__package", "booking__user")
            .prefetch_related("photos")
        )


class PublicPackageReviewListView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        package_id = self.kwargs["package_id"]

        return (
            Review.objects
            .filter(
                booking__package_id=package_id,
                status="approved",
            )
            .select_related("booking", "booking__package", "booking__user")
            .prefetch_related("photos")
        )


class ManagerReviewListView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsManager]

    def get_queryset(self):
        return (
            Review.objects
            .select_related("booking", "booking__package", "booking__user")
            .prefetch_related("photos")
        )

