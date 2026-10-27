from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Destination(models.Model):
    name = models.CharField(max_length=200)
    state = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    description = models.TextField()
    categories = models.ManyToManyField(
    Category,
    related_name="categorized_destinations",
    blank=True
    )
    image = models.ImageField(
        upload_to="destinations/",
        blank=True,
        null=True
    )
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favorites"
    )
    destination = models.ForeignKey(
        "destinations.Destination",
        on_delete=models.CASCADE,
        related_name="favorited_by"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "destination"],
                name="unique_user_favorite_destination"
            )
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.destination.name}"
