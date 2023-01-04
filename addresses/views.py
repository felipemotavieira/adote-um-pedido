from rest_framework.views import APIView, Request, Response, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics
from .models import Address
from .serializers import AddressSerializer
from .permissions import IsUserOrInstitutionAddress
import ipdb

# Create your views here.
class AddressView(generics.ListCreateAPIView):
    # ipdb.set_trace()
    authentication_classes = [JWTAuthentication]

    serializer_class = AddressSerializer
    queryset = Address.objects.all()


class AddressDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = AddressSerializer
    queryset = Address.objects.all()

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsUserOrInstitutionAddress]
