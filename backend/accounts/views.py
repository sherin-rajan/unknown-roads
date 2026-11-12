from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserProfile
from .permissions import IsCustomer, IsManager
from .serializers.register import (RegisterSerializer,CurrentUserSerializer,)
from .serializers.profile import CustomerProfileSerializer
from .serializers.password import ChangePasswordSerializer
from apps.destinations.models import Favorite, Destination
from .serializers.favorite import FavoriteSerializer
from django.utils import timezone
from apps.packages.models import (
    TravelPackage,
    PackageBooking,
    PackageEnquiry,
)
from apps.notifications.models import Notification

@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({
            "message": "Your Unknown Roads account has been created successfully.",
            "user": CurrentUserSerializer(user).data,
        }, status=status.HTTP_201_CREATED)
    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def current_user(request):
    serializer = CurrentUserSerializer(request.user)
    return Response(serializer.data)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_view(request):
    refresh_token = request.data.get("refresh")
    if not refresh_token:
        return Response(
            {"error": "Refresh token is required."},
            status=status.HTTP_400_BAD_REQUEST
        )
    try:
        token = RefreshToken(refresh_token)
        token.blacklist()
    except TokenError:
        return Response(
            {"error": "Invalid or expired refresh token."},
            status=status.HTTP_400_BAD_REQUEST
        )
    return Response(
        {"message": "Logout successful."},
        status=status.HTTP_200_OK
    )

@api_view(["GET", "PATCH", "PUT"])
@permission_classes([IsAuthenticated, IsCustomer])
def customer_profile(request):
    profile = request.user.profile

    if request.method == "GET":
        serializer = CustomerProfileSerializer(profile)
        return Response(serializer.data)

    serializer = CustomerProfileSerializer(
        profile,
        data=request.data,
        partial=(request.method == "PATCH")
    )

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def change_password(request):
    serializer = ChangePasswordSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    user = request.user

    if not user.check_password(serializer.validated_data["old_password"]):
        return Response(
            {"old_password": ["Your current password is incorrect."]},
            status=status.HTTP_400_BAD_REQUEST
        )

    user.set_password(serializer.validated_data["new_password"])
    user.save()

    return Response(
        {
            "message": "Password changed successfully. Please log in again."
        },
        status=status.HTTP_200_OK
    )


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def customer_favorites(request):
    if request.method == "GET":
        favorites = Favorite.objects.filter(
            user=request.user
        ).select_related("destination")

        serializer = FavoriteSerializer(
            favorites,
            many=True,
            context={"request": request}
        )
        return Response(serializer.data)

    destination_id = request.data.get("destination")

    if not destination_id:
        return Response(
            {"error": "Destination ID is required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        destination = Destination.objects.get(id=destination_id)
    except (Destination.DoesNotExist, ValueError, TypeError):
        return Response(
            {"error": "Destination not found."},
            status=status.HTTP_404_NOT_FOUND
        )

    favorite, created = Favorite.objects.get_or_create(
        user=request.user,
        destination=destination
    )

    serializer = FavoriteSerializer(
        favorite,
        context={"request": request}
    )

    if created:
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(
        {
            "message": "This destination is already in your favorites.",
            "favorite": serializer.data
        },
        status=status.HTTP_200_OK
    )


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def remove_favorite(request, favorite_id):
    try:
        favorite = Favorite.objects.get(
            id=favorite_id,
            user=request.user
        )
    except Favorite.DoesNotExist:
        return Response(
            {"error": "Favorite not found."},
            status=status.HTTP_404_NOT_FOUND
        )

    favorite.delete()

    return Response(
        {"message": "Destination removed from favorites."},
        status=status.HTTP_200_OK
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsCustomer])
def customer_dashboard(request):
    user = request.user
    today = timezone.localdate()

    bookings = PackageBooking.objects.filter(user=user)

    return Response({
        "total_bookings": bookings.count(),

        "upcoming_trips": bookings.filter(
            booking_status="confirmed",
            departure__start_date__gte=today
        ).count(),

        "pending_bookings": bookings.filter(
            booking_status="pending"
        ).count(),

        "total_enquiries": PackageEnquiry.objects.filter(
            user=user
        ).count(),

        "unread_notifications": Notification.objects.filter(
            recipient=user,
            is_read=False
        ).count(),
    })


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsManager])
def manager_dashboard(request):
    return Response({
        "total_packages": TravelPackage.objects.count(),

        "published_packages": TravelPackage.objects.filter(
            publication_status="published"
        ).count(),

        "total_bookings": PackageBooking.objects.count(),

        "pending_bookings": PackageBooking.objects.filter(
            booking_status="pending"
        ).count(),

        "new_enquiries": PackageEnquiry.objects.filter(
            status="pending"
        ).count(),

        "unread_notifications": Notification.objects.filter(
            recipient=request.user,
            is_read=False
        ).count(),
    })