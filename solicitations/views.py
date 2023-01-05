from .serializers import SolicitationSerialzer
from .models import Solicitation
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from donees.models import Donee
from .permissions import IsInstitutionDoneeSame


class SolicitationView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]

    permission_classes = [IsInstitutionDoneeSame]

    serializer_class = SolicitationSerialzer
    queryset = Solicitation.objects.all()


    def perform_create(self, serializer):
        donee = Donee.objects.get(donee = self.kwargs["pk"])
        serializer.save(user = self.request.user, donee = donee)


    def get_queryset(self):
        return self.queryset.filter(donee_id = self.kwargs["pk"])



class SolicitationDetailView(generics.RetrieveUpdateAPIView):
    authentication_classes = [JWTAuthentication]

    permission_classes = [IsInstitutionDoneeSame]

    serializer_class = SolicitationSerialzer
    queryset = Solicitation.objects.all()
    
