from django.contrib import admin
from .models import Category, Destination

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "state", "is_featured")
    list_display_links = ("name",)
    list_filter = ("state", "is_featured")
    search_fields = ("name", "state", "location")
    list_editable = ("is_featured",)
    filter_horizontal = ("categories",)
