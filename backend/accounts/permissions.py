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


