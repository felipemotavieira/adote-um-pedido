from rest_framework import permissions
from rest_framework.views import Request, View
from .models import Address

class IsUserOrInstitutionAddress(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, obj: Address):
        if request.user.address_id == obj.id:
            return True

        return request.user.is_superuser