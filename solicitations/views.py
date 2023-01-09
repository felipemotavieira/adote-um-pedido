from rest_framework import generics, views
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from donees.models import Donee
from users.models import User
from .permissions import IsInstitutionDoneeSame, IsStaffOrReadOnly, IsDonor, IsDonorSolicitationUser
from .serializers import SolicitationSerializer
from .models import Solicitation, StatusChoices
import ipdb

class SolicitationView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStaffOrReadOnly]

    serializer_class = SolicitationSerializer
    queryset = Solicitation.objects.all()

    def perform_create(self, serializer):
        donee = Donee.objects.get(id = self.request.data['donee'])
        serializer.save(donee = donee)


class SolicitationDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsInstitutionDoneeSame]

    serializer_class = SolicitationSerializer
    queryset = Solicitation.objects.all()

    # def perform_destroy(self, instance):
    #     instance.status = StatusChoices.DISABLE
    #     instance.save()

    lookup_url_kwarg = "solicitation_id"

class SolicitationAtributionView(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsDonor]

    def patch(self, request, solicitation_id):
        solicitation = get_object_or_404(Solicitation, id=solicitation_id)

        if not solicitation.user:
            solicitation.user = request.user

        self.check_object_permissions(request, solicitation)
        
        if solicitation.status == 'Não informado':
            data = {'status': 'Disponível'}

        if solicitation.status == 'Disponível':
            data = {'status': 'Não disponível'}

        if solicitation.status == 'Não disponível':
            data = {'status': 'Enviado'}

        if solicitation.status == 'Enviado':
            data = {'status': 'Recebido'}

        serializer = SolicitationSerializer(solicitation, data=data, partial=True)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return views.Response(serializer.data)

class SolicitationDropView(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsDonorSolicitationUser]

    def patch(self, request, solicitation_id):
        solicitation = get_object_or_404(Solicitation, id=solicitation_id)

        self.check_object_permissions(request, solicitation)

        solicitation.user.clear()

        solicitation.save()

        return solicitation
