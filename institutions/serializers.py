from rest_framework import serializers
from .models import Institution


class InstitutionSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()

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
