from rest_framework import generics
from .serializers import DoneeSerializers
from .models import Donee
from .permissions import IsAdmin
from rest_framework_simplejwt.authentication import JWTAuthentication


class doneeView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]
    serializer_class = DoneeSerializers
    queryset = Donee.objects.all()
    

class doneeDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]
    serializer_class = DoneeSerializers
    queryset = Donee.objects.all()
    