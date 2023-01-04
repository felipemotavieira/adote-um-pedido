from rest_framework.views import APIView, Request, Response, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics
from .models import Address
from .serializer import AddressSerializer
from .permissions import IsUserOrInstitutionAddress

# Create your views here.
class AddressView(generics.ListCreateAPIView):
    serializer_class = AddressSerializer
    queryset = Address.objects.all()

class AddressDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = AddressSerializer
    queryset = Address.objects.all()

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsUserOrInstitutionAddress]
