from rest_framework import permissions
from rest_framework.views import Request, View
from .models import Address
from institutions.models import Institution


class IsUserOrInstitutionAddress(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, obj: Address):
        institution = Institution.objects.filter(address_id=view.kwargs["address_id"])

        if request.user.is_staff and institution:
            return True

        if request.user.address_id == obj.id:
            return True

        return request.user.is_superuser
