from rest_framework import permissions
from rest_framework.views import Request, View
from users.models import User
from .models import Institution


class IsStaffOrReadOnly(permissions.BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True

        if (
            request.user.is_authenticated
            and request.user.is_staff
            or request.user.is_superuser
        ):
            return True

        return False


class IsInstitutionOwner(permissions.BasePermission):
    def has_object_permission(
        self, request, view: View, institution: Institution
    ) -> bool:
        if (
            request.user.is_authenticated
            and request.user.is_superuser
            or request.user == institution.owner
        ):
            return True

        return False
