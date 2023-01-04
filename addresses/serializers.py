from rest_framework import serializers
from .models import Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address

        fields = '__all__'

    def create(self, validated_data):
        created_address = Address.objects.create(**validated_data)
        user = self.context['request'].user
        
        setattr(user, 'address', created_address)
        user.save()
        
        return created_address

    def update(self, instance: Address, validated_data: dict):
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance