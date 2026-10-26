from rest_framework.permissions import BasePermission

class IsCustomer(BasePermission):
    """Allow access only to customer accounts."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and hasattr(request.user, "profile")
            and request.user.profile.role == "customer"
        )

class IsManager(BasePermission):
    """Allow access only to manager accounts."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and hasattr(request.user, "profile")
            and request.user.profile.role == "manager"
        )

class IsPlatformAdmin(BasePermission):
    """Allow access only to accounts assigned the admin role."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and hasattr(request.user, "profile")
            and request.user.profile.role == "admin"
        )

class IsManagerOrPlatformAdmin(BasePermission):
    """Allow managers and platform admins."""

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if not hasattr(request.user, "profile"):
            return False

        return request.user.profile.role in ["manager", "admin"]
