from rest_framework import permissions
from rest_framework.views import Request, View
from .models import Address
from institutions.models import Institution
import ipdb

class IsAuthenticated(permissions.BasePermission):
    def has_permission(self, request: Request, view: View):
        return request.user.is_authenticated


class IsUserOrInstitutionAddress(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, obj: Address):
        institution = Institution.objects.filter(address_id = view.kwargs["address_id"])

        if institution:
            return True

        if request.user.is_authenticated and request.user.address_id == obj.id:
            return True

        return request.user.is_superuser
