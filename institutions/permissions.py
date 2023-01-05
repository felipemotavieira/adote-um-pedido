from rest_framework import permissions
from rest_framework.views import Request, View
from .models import Institution


class IsStaffOrReadOnly(permissions.BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True

        if (
            request.user.is_authenticated
            and request.user.is_superuser
        ):
            return True

        return False


class IsInstitutionOwner(permissions.BasePermission):
    def has_object_permission(
        self, request, view: View, institution: Institution
    ) -> bool:

        return request.user == institution.owner and request.user.is_staff

