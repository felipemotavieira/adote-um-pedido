from rest_framework import permissions
from rest_framework.views import Request, View
from .models import Solicitation
from donees.models import Donee
import ipdb

class IsStaffOrReadOnly(permissions.BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True

        donee = Donee.objects.get(id = request.data['donee'])

        if (
            request.user.is_authenticated
            and request.user.is_superuser or request.user == donee.institution.owner
        ):
            return True

        return False



class IsInstitutionDoneeSame(permissions.BasePermission):
    def has_object_permission(self, request, view: View, solicitation: Solicitation) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True

        solicitation = Solicitation.objects.get(id = view.kwargs["solicitation_id"])

        if (request.user.is_authenticated and request.user.is_superuser or request.user.id == solicitation.donee.institution.owner.id):
            return True

        return False
