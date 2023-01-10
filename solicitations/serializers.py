from rest_framework import serializers
from .models import Solicitation
from donees.models import Donee
import ipdb

class SolicitationSerializer(serializers.ModelSerializer):
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
            "institution"
        ]
        read_only_fields = ["user","institution","created_at","updated_at"]



    def create(self, validated_data: dict) -> Solicitation:
        return Solicitation.objects.create(**validated_data)


    
    def update(self, instance: Solicitation, validated_data: dict) -> Solicitation:
        for key, value in validated_data.items():
            setattr(instance,key,value)
        
        instance.save()
        return instance