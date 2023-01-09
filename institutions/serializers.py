from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from .models import Institution
from rest_framework.exceptions import PermissionDenied


class InstitutionSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()

    cnpj = serializers.IntegerField(
        validators=[
            UniqueValidator(
                queryset=Institution.objects.all(),
                message="CNPJ already exists.",
            )
        ],
    )

    class Meta:
        model = Institution
        fields = [
            "id",
            "name",
            "email",
            "cnpj",
            "phone",
            "type",
            "is_active",
            "created_at",
            "updated_at",
            "status",
            "owner",
            "address",
        ]
        read_only_fields = ["owner", "address"]

    def get_owner(self, obj):
        return {
            "id": obj.owner.id,
            "first_name": obj.owner.first_name,
            "last_name": obj.owner.last_name,
            "username": obj.owner.username,
            "email": obj.owner.email,
            "created_at": obj.owner.created_at,
            "updated_at": obj.owner.updated_at,
        }

    def update(self, instance: Institution, validated_data: dict) -> Institution:
        user = self.context["request"].user

        for key, value in validated_data.items():
            if key == "status":
                if user.is_superuser is True:
                    setattr(instance, key, value)
                else:
                    raise PermissionDenied
            else:
                setattr(instance, key, value)

        instance.save()

        return instance
