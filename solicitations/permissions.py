from rest_framework import permissions
from rest_framework.views import Request, View
from .models import Solicitation
from donees.models import Donee
from django.shortcuts import get_object_or_404


class IsStaffOrReadOnly(permissions.BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True

        donee = get_object_or_404(Donee,id = request.data['donee'])

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

        solicitation = get_object_or_404(Solicitation,id = view.kwargs["solicitation_id"])

        if (request.user.is_authenticated and request.user.is_superuser or request.user.id == solicitation.donee.institution.owner.id):
            return True

        return False


class IsDonor(permissions.BasePermission):
    def has_object_permission(self, request, view: View, solicitation: Solicitation) -> bool:
        if request.user.is_superuser:
            return True
        
        if request.user.is_staff:
            return False

        if solicitation.user and solicitation.user == request.user:
            return True

        return False

class IsDonorSolicitationUser(permissions.BasePermission):
    def has_object_permission(self, request, view: View, solicitation: Solicitation) -> bool:
        return solicitation.user == request.user