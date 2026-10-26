from django.contrib import admin
from .models import UserProfile

# Register your models here.

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "created_at")
    list_filter = ("role",)
    search_fields = ("user__username", "user__email")
    readonly_fields = ("created_at", "updated_at")

    def has_add_permission(self, request):
        # Profiles are created automatically for users.
        return False

    def has_change_permission(self, request, obj=None):
        # Only a Django superuser can assign or change roles.
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        # Keep profiles protected from accidental deletion.
        return False
