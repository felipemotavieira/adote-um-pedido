from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics

from .permissions import IsAdminOrCreateOnly, IsAdminOrProfileOwner
from .serializers import UserSerializer
from .models import User


class UserView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrCreateOnly]

    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrProfileOwner]

    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

    lookup_url_kwarg = "user_id"
