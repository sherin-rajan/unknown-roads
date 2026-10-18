
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from rest_framework import status

from .models import Destination, Category
from .serializers import DestinationSerializer, CategorySerializer

@api_view(['GET','POST'])
def destination_list(request):
    if request.method == 'GET':
        destinations = Destination.objects.all().order_by('-is_featured','-created_at')

        ordering = request.query_params.get('ordering')

        if ordering == 'featured':
            destinations = destinations.order_by('-is_featured', '-created_at')
        elif ordering == 'newest':
            destinations = destinations.order_by('-created_at')
        elif ordering == 'name':
            destinations = destinations.order_by('name')

        #filter by category
        category_name = request.query_params.get('category')
        if category_name:
            destinations = destinations.filter(
                categories__name__iexact=category_name
            ).distinct()

        state_name = request.query_params.get('state')
        if state_name:
            destinations = destinations.filter(
                state__iexact=state_name
            )

        # Search destinations by name or location
        search_query = request.query_params.get('search')
        if search_query:
            destinations = destinations.filter(
                Q(name__icontains=search_query) |
                Q(state__icontains=search_query) |
                Q(location__icontains=search_query)
            ).distinct()
        paginator = PageNumberPagination()
        paginator.page_size = 5
        page = paginator.paginate_queryset(destinations, request)

        serializer = DestinationSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    elif request.method == 'POST':
        serializer = DestinationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def destination_detail(request, pk):
    try:
        destination = Destination.objects.get(pk=pk)
    except Destination.DoesNotExist:
        return Response({"error": "Destination not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DestinationSerializer(destination)
        return Response(serializer.data)

    elif request.method in ['PUT', 'PATCH']:
        serializer = DestinationSerializer(destination, data=request.data, partial=(request.method == 'PATCH'))

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        destination.delete()
        return Response({"message": "Destination deleted successfully"}, status=status.HTTP_200_OK)

@api_view(['GET'])
def featured_destinations(request):
    destinations = Destination.objects.filter(is_featured=True ).order_by('-created_at')
    serializer = DestinationSerializer(destinations, many=True)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
def category_list(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def category_detail(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response(
            {"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND
        )

    serializer = CategorySerializer(category)
    return Response(serializer.data)
