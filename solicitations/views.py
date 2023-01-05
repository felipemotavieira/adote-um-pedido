from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from donees.models import Donee
from users.models import User
from .permissions import IsInstitutionDoneeSame, IsStaffOrReadOnly
from .serializers import SolicitationSerialzer
from .models import Solicitation, StatusChoices

class SolicitationView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]

    # permission_classes = [IsInstitutionDoneeSame]
    permission_classes = [IsStaffOrReadOnly]

    serializer_class = SolicitationSerialzer
    queryset = Solicitation.objects.all()


    def perform_create(self, serializer):
        donee = Donee.objects.get(id = self.kwargs["pk"])
        serializer.save(user = self.request.user, donee = donee)




class SolicitationDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]

    permission_classes = [IsInstitutionDoneeSame]

    serializer_class = SolicitationSerialzer
    queryset = Solicitation.objects.all()



    def perform_destroy(self, instance):
        instance.status = StatusChoices.DISABLE
        instance.save()