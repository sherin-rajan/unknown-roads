from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsCustomer(BasePermission):
    """Allow customer accounts and Django superusers."""

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        if user.is_superuser:
            return True

        return (
            hasattr(user, "profile")
            and user.profile.role == "customer"
        )


class IsManager(BasePermission):
    """Allow manager accounts and Django superusers."""

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        if user.is_superuser:
            return True

        return (
            hasattr(user, "profile")
            and user.profile.role == "manager"
        )


class ReadOnlyOrManager(BasePermission):
    """
    Allow everyone to read.
    Only managers and Django superusers can create, update or delete.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return IsManager().has_permission(request, view)
