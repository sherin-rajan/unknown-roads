from django.contrib import admin

from .models import (
    PackageCategory,
    TravelPackage,
    GroupSize,
    PackageDay,
    PackageDeparture,
    PackageEnquiry,
    PackageBooking,
    BookingTraveller,
    BookingStatusHistory,
)


@admin.register(PackageCategory)
class PackageCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(GroupSize)
class GroupSizeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "capacity")
    ordering = ("capacity",)


@admin.register(TravelPackage)
class TravelPackageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "main_destination",
        "trip_mode",
        "group_type",
        "status",
        "publication_status",
    )
    list_filter = (
        "trip_mode",
        "group_type",
        "status",
        "publication_status",
        "categories",
    )
    search_fields = ("name", "main_destination__name")
    filter_horizontal = ("categories",)


@admin.register(PackageDay)
class PackageDayAdmin(admin.ModelAdmin):
    list_display = ("id", "package", "day_number", "title")
    list_filter = ("package",)
    ordering = ("package", "day_number")


@admin.register(PackageDeparture)
class PackageDepartureAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "package",
        "start_date",
        "end_date",
        "price_per_person",
        "group_size",
        "total_seats",
        "available_seats",
        "availability_status",
    )
    list_filter = ("availability_status", "group_size")
    search_fields = ("package__name",)
    ordering = ("start_date",)


@admin.register(PackageEnquiry)
class PackageEnquiryAdmin(admin.ModelAdmin):
    list_display = ("id", "package", "user", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("package__name", "user__username")


class BookingTravellerInline(admin.TabularInline):
    model = BookingTraveller
    extra = 0


class BookingStatusHistoryInline(admin.TabularInline):
    model = BookingStatusHistory
    extra = 0
    can_delete = False
    readonly_fields = (
        "old_status",
        "new_status",
        "changed_by",
        "note",
        "changed_at",
    )


@admin.register(PackageBooking)
class PackageBookingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "booking_reference",
        "user",
        "package",
        "departure",
        "number_of_travellers",
        "total_amount",
        "booking_status",
        "booked_at",
    )
    list_filter = ("booking_status", "traveller_type")
    search_fields = (
        "booking_reference",
        "user__username",
        "package__name",
    )
    readonly_fields = (
        "booking_reference",
        "price_per_person",
        "total_amount",
        "booked_at",
        "updated_at",
    )
    inlines = [
        BookingTravellerInline,
        BookingStatusHistoryInline,
    ]


@admin.register(BookingTraveller)
class BookingTravellerAdmin(admin.ModelAdmin):
    list_display = ("id", "booking", "full_name", "age")
    search_fields = ("full_name",)


@admin.register(BookingStatusHistory)
class BookingStatusHistoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "booking",
        "old_status",
        "new_status",
        "changed_by",
        "changed_at",
    )
    list_filter = ("new_status",)
    readonly_fields = (
        "booking",
        "old_status",
        "new_status",
        "changed_by",
        "note",
        "changed_at",
    )