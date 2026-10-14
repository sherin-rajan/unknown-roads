from django.db import models

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
