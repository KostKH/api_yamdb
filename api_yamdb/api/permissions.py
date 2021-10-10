from rest_framework import permissions


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsAdmin(permissions.BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        if not request.user:
            return False
        if not request.user.is_authenticated:
            return False
        return bool(
            request.user.is_staff or 
            request.user.role == 'admin' or 
            request.user.is_superuser
        )
