from rest_framework.validators import UniqueValidator
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="Email already exists.",
            )
        ],
    )

    cpf = serializers.CharField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="CPF already exists.",
            )
        ],
    )

    def create(self, validated_data: dict) -> User:
        return User.objects.create_user(**validated_data)

    def update(self, instance: User, validated_data: dict) -> User:
        for key, value in validated_data.items():
            if key == "password":
                instance.set_password(value)
            else:
                setattr(instance, key, value)

        instance.save()

        return instance

    class Meta:
        model = User
        depth = 1
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
            "cpf",
            "is_active",
            "is_superuser",
            "is_staff",
            "created_at",
            "updated_at",
            "address",
        ]

        read_only_fields = ["created_at", "updated_at", "address"]
        extra_kwargs = {"password": {"write_only": True}}
