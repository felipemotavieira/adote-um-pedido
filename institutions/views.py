from .serializers import InstitutionSerializer
from .models import Institution
from .exceptions import UserAlreadyHasInstitution
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import IsStaffOrReadOnly, IsInstitutionOwner
import ipdb

class InstitutionView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStaffOrReadOnly]

    serializer_class = InstitutionSerializer
    queryset = Institution.objects.all()

    def perform_create(self, serializer):
        if self.request.user.institution:
            raise UserAlreadyHasInstitution
        ipdb.set_trace()
        serializer.save(owner=self.request.user)


class InstitutionDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsInstitutionOwner]

    serializer_class = InstitutionSerializer
    queryset = Institution.objects.all()

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
