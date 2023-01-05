from rest_framework import serializers

from .exceptions import InstitutionDoesNotExist
from institutions.models import Institution
from .models import Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address

        fields = "__all__"

    def create(self, validated_data):
        created_address = Address.objects.create(**validated_data)
        user = self.context["request"].user

        if user.is_staff is True and not user.is_superuser:
            institution = Institution.objects.get(owner=user)

            if not institution:
                raise InstitutionDoesNotExist

            setattr(institution, "address", created_address)
            institution.save()

            return created_address

        setattr(user, "address", created_address)
        user.save()

        return created_address

    def update(self, instance: Address, validated_data: dict):
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance
