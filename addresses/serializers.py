from rest_framework import serializers
from .models import Address

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address

        fields = '__all__'

    def create(self, validated_data):
        return Address.objects.create(**validated_data)

    def update(self, instance: Address, validated_data: dict):
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance
