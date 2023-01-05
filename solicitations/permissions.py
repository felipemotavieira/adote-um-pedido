from rest_framework import permissions
from rest_framework.views import Request, View
from .models import Solicitation



class IsInstitutionDoneeSame(permissions.BasePermission):
    def has_object_permission(self, request, view: View, solicitation: Solicitation) -> bool:
        if (request.user.is_authenticated and request.user.is_superuser or request.user.id == solicitation.donee.institution.owner):
            return True

        return False