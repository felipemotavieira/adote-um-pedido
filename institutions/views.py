from .serializers import InstitutionSerializer
from .models import Institution
from .exceptions import UserAlreadyHasInstitution
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import IsStaffOrReadOnly, IsInstitutionOwner
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings


class InstitutionView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStaffOrReadOnly]

    serializer_class = InstitutionSerializer
    queryset = Institution.objects.all()

    def perform_create(self, serializer):
        if hasattr(self.request.user, "institution"):
            raise UserAlreadyHasInstitution

        send_mail(
            subject="Solicitação recebida",
            message=f"Olá, {self.request.user}. \nA solicitação de criação da nova instituição foi recebida e no momento estamos validando os dados para a criação.",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.request.user.email],
            fail_silently=False,
        )
        send_mail(
            subject="Solicitação recebida",
            message=f'Olá, {self.request.data["name"]}. \nA solicitação de criação da nova instituição foi recebida e no momento estamos validando os dados para a criação.',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.request.data["email"]],
            fail_silently=False,
        )

        serializer.save(owner=self.request.user)


class InstitutionDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsInstitutionOwner]

    serializer_class = InstitutionSerializer
    queryset = Institution.objects.all()

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
