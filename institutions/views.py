from .serializers import InstitutionSerializer
from .models import Institution
from rest_framework import generics


class InstitutionView(generics.ListCreateAPIView):
    serializer_class = InstitutionSerializer
    queryset = Institution.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class InstitutionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = InstitutionSerializer
    queryset = Institution.objects.all()

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
