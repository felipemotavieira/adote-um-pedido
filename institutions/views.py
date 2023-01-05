from .serializers import InstitutionSerializer
from .models import Institution
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import IsStaffOrReadOnly, IsInstitutionOwner


class InstitutionView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStaffOrReadOnly]

    serializer_class = InstitutionSerializer
    queryset = Institution.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class InstitutionDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsInstitutionOwner]

    serializer_class = InstitutionSerializer
    queryset = Institution.objects.all()

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
