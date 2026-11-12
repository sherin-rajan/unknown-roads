from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from apps.packages.models import PackageBooking


class Review(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending Approval"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    booking = models.OneToOneField(
        PackageBooking,
        on_delete=models.CASCADE,
        related_name="review",
    )

    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ]
    )

    feedback = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.booking.user.username} - {self.rating}/5"


class ReviewPhoto(models.Model):

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="photos",
    )

    image = models.ImageField(upload_to="reviews/")

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo for review {self.review_id}"

