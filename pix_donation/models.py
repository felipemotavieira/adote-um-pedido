import uuid
from django.db import models


class PixDonation(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    registered_at = models.DateTimeField(auto_now_add=True)
    value = models.DecimalField(max_digits=8, decimal_places=2)

    donee_institution = models.ForeignKey(
        "institutions.Institution",
        on_delete=models.CASCADE,
        related_name="pix_donation",
    )

    donor = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="user_pix_donation",
    )
