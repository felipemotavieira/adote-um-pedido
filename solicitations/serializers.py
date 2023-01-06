from rest_framework import serializers
from .models import Solicitation
from donees.models import Donee


class SolicitationSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Solicitation
        fields = [
            "id",
            "description",
            "status",
            "created_at",
            "updated_at",
            "user_id",
            "donee_id",
        ]
        read_only_fields = ["user"]



    def create(self, validated_data: dict) -> Solicitation:
        return Solicitation.objects.create(**validated_data)


    
    def update(self, instance: Solicitation, validated_data: dict) -> Solicitation:
        for key, value in validated_data.items():
            setattr(instance,key,value)
        
        instance.save()

        return instance