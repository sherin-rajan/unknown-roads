from django.contrib import admin
from .models import Trip, TripDestination

# Register your models here.

class TripDestinationInline(admin.TabularInline):
    model = TripDestination
    extra = 1


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "user",
        "start_date",
        "end_date",
        "created_at",
    )
    list_filter = ("start_date", "end_date", "created_at")
    search_fields = ("name", "user__username")
    inlines = [TripDestinationInline]


@admin.register(TripDestination)
class TripDestinationAdmin(admin.ModelAdmin):
    list_display = ("trip", "destination", "visit_date", "order")
    list_filter = ("visit_date",)
    search_fields = ("trip__name", "destination__name")