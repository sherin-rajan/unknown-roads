from django.contrib.auth.models import User
from django.db import models
from apps.destinations.models import Destination

class Trip(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="trips"
    )
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.user.username}"

class TripDestination(models.Model):
    trip = models.ForeignKey(
        Trip,
        on_delete=models.CASCADE,
        related_name="itinerary_items"
    )
    destination = models.ForeignKey(
        Destination,
        on_delete=models.CASCADE,
        related_name="trip_items"
    )
    visit_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "id"]
        constraints = [
            models.UniqueConstraint(
                fields=["trip", "destination"],
                name="unique_destination_per_trip"
            )
        ]

    def __str__(self):
        return f"{self.trip.name} - {self.destination.name}"
