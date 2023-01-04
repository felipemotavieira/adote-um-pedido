from rest_framework import permissions


class IsAdminOrCreateOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated and request.user.is_superuser

        return True


class IsAdminOrProfileOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, user):
        if request.user.is_authenticated and request.user.is_superuser:
            return True

        return user == request.user
