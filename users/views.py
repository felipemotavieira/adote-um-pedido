from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics

from .permissions import IsAdminOrCreateOnly, IsAdminOrProfileOwner
from .serializers import UserSerializer
from .models import User
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings


class UserView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrCreateOnly]

    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        serializer.save()
        user = self.request.data
        send_mail(
            subject="Sua conta no AdoteUmPedito foi criada",
            message=f"""
                Olá, {user["first_name"]}.
                    Sua conta no Adote Um Pedito foi criada com sucesso!
            """,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user["email"]],
            fail_silently=False,
        )


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrProfileOwner]

    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_destroy(self, instance):
        email = instance.email
        instance.is_active = False
        instance.save()
        send_mail(
            subject="Conta Deletada",
            message=f"Sua conta no Adote Um Pedito foi excluida com sucesso!",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )

    lookup_url_kwarg = "user_id"
