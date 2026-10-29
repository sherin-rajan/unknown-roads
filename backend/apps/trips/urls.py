from django.urls import path
from . import views

urlpatterns = [
    path("", views.trip_list_create, name="trip-list-create"),
    path("<int:trip_id>/", views.trip_detail, name="trip-detail"),
    path(
        "<int:trip_id>/itinerary/",
        views.itinerary_list_create,
        name="itinerary-list-create",
    ),
    path(
        "<int:trip_id>/itinerary/<int:item_id>/",
        views.itinerary_detail,
        name="itinerary-detail",
    ),
]