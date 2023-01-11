from rest_framework import serializers
from pix_donation.models import PixDonation


class PixDonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PixDonation
        depth = 1
        fields = [
            "id",
            "value",
            "institution",
            "registered_at",
            "donee_institution",
            "donor",
        ]

        read_only_fields = ["registered_at", "donor"]
