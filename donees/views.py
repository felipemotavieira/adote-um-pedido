from rest_framework import generics
from .serializers import DoneeSerializers
from .models import Donee
from .permissions import isAdmOrStaff, isAdmOwner
from rest_framework_simplejwt.authentication import JWTAuthentication
from institutions.models import Institution
from django.shortcuts import get_object_or_404


class doneeView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [isAdmOrStaff]
    serializer_class = DoneeSerializers
    queryset = Donee.objects.all()

    def perform_create(self, serializer):
        institution = get_object_or_404(Institution, pk=self.request.data['institution'])
        serializer.save(institution=institution)



class doneeDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [isAdmOwner]
    serializer_class = DoneeSerializers
    queryset = Donee.objects.all()
    