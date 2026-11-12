from django.contrib import admin

from .models import Review, ReviewPhoto


class ReviewPhotoInline(admin.TabularInline):
    model = ReviewPhoto
    extra = 0


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "booking",
        "rating",
        "status",
        "created_at",
    ]

    list_filter = ["status", "rating", "created_at"]
    search_fields = [
        "booking__user__username",
        "booking__package__name",
        "feedback",
    ]

    list_editable = ["status"]
    inlines = [ReviewPhotoInline]
