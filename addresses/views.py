from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from .permissions import IsUserOrInstitutionAddress
from .serializers import AddressSerializer
from .models import Address


class AddressView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = AddressSerializer
    queryset = Address.objects.all()


class AddressDetailView(generics.RetrieveUpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsUserOrInstitutionAddress]

    serializer_class = AddressSerializer
    queryset = Address.objects.all()

    lookup_url_kwarg = "address_id"
