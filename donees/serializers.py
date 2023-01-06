from rest_framework import serializers
from .models import Donee
class DoneeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Donee
        fields = '__all__'
        read_only_fields = ['created_at' ,'updated_at', 'institution']
        depth = 1

    def get_institution(self, obj):
        return obj

   