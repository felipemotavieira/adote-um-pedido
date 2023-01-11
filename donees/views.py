from rest_framework import generics
from .serializers import DoneeSerializers
from .models import Donee
from .permissions import isAdmOrStaff, isAdmOwner
from rest_framework_simplejwt.authentication import JWTAuthentication
from institutions.models import Institution
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings


class doneeView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [isAdmOrStaff]
    serializer_class = DoneeSerializers
    queryset = Donee.objects.all()

    def perform_create(self, serializer):
        institution = get_object_or_404(Institution, pk=self.request.data['institution'])
        serializer.save(institution=institution)

        owner = self.request.user
        donee = self.request.data
        institutions = Institution.objects.all()
        institution = institutions.filter(id=donee["institution"]).values()[0]

        send_mail(
            subject="Registro de Donatário",
            message=f"""
                Olá, {owner.first_name}.
                    O donatário {donee['name']} foi registrado com sucesso na instituição {institution['name']}
            """,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[owner.email],
            fail_silently=False,
        )
        send_mail(
            subject="Registro de Donatário",
            message=f"""
                Olá, {institution['name']}.
                    O donatário {donee['name']} foi registrado com sucesso na instituição {institution['name']}
            """,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[institution["email"]],
            fail_silently=False,
        )


class doneeDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [isAdmOwner]
    serializer_class = DoneeSerializers
    queryset = Donee.objects.all()
    