from rest_framework import permissions
from institutions.models import Institution
from donees.models import Donee


class isAdmOrStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        institution = Institution.objects.get(id = request.data["institution"])

        if request.user.id == institution.owner.id or request.user.is_superuser:
            return True

        return False

class isAdmOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        donee = Donee.objects.get(id = view.kwargs["pk"])

        if request.user == donee.institution.owner or request.user.is_superuser:
            return True
       

        return False
