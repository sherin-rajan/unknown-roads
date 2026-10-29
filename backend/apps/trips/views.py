from rest_framework import status
from rest_framework.decorators import (api_view, permission_classes)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Trip
from .serializers.trip import TripSerializer
from datetime import date
from apps.destinations.models import Destination
from .models import TripDestination
from .serializers.itinerary import TripDestinationSerializer

@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def trip_list_create(request):
    if request.method == "GET":
        trips = Trip.objects.filter(user=request.user)
        serializer = TripSerializer(trips, many=True)
        return Response(serializer.data)

    serializer = TripSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST,
    )


@api_view(["GET", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def trip_detail(request, trip_id):
    try:
        trip = Trip.objects.get(
            id=trip_id,
            user=request.user,
        )
    except Trip.DoesNotExist:
        return Response(
            {"error": "Trip not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    if request.method == "GET":
        serializer = TripSerializer(trip)
        return Response(serializer.data)

    if request.method == "PATCH":
        serializer = TripSerializer(
            trip,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    trip.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def itinerary_list_create(request, trip_id):
    try:
        trip = Trip.objects.get(
            id=trip_id,
            user=request.user,
        )
    except Trip.DoesNotExist:
        return Response(
            {"error": "Trip not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    if request.method == "GET":
        items = TripDestination.objects.filter(
            trip=trip
        ).select_related("destination")

        serializer = TripDestinationSerializer(items, many=True)
        return Response(serializer.data)

    serializer = TripDestinationSerializer(data=request.data, context={"trip": trip})

    if serializer.is_valid():
        serializer.save(trip=trip)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST,
    )


@api_view(["PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def itinerary_detail(request, trip_id, item_id):
    try:
        item = TripDestination.objects.get(
            id=item_id,
            trip_id=trip_id,
            trip__user=request.user,
        )
    except TripDestination.DoesNotExist:
        return Response(
            {"error": "Itinerary item not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    if request.method == "PATCH":
        serializer = TripDestinationSerializer(
                item,
                data=request.data,
                partial=True,
                context={"trip": item.trip}
                )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    item.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)