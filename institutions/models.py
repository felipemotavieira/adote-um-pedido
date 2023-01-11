from django.db import models
import uuid

class TypeChoice(models.TextChoices):
    ORFANATO = "Orfanato"
    ASILO = "Asilo"
    NOT_INFORMED = "Não informado"


class StatusChoices(models.TextChoices):
    UNDER_EXAMINATION = "Under examination"
    APPROVED = "Approved"

class Institution(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    cnpj = models.CharField(max_length=14, unique=True)
    phone = models.CharField(max_length=16)
    type = models.CharField(
        max_length=20,
        choices=TypeChoice.choices,
        default=TypeChoice.NOT_INFORMED,
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.UNDER_EXAMINATION,
    )

    address = models.OneToOneField(
        "addresses.Address",
        on_delete=models.CASCADE,
        related_name="institution",
        null=True,
    )

    owner = models.OneToOneField(
        "users.User",
        on_delete=models.CASCADE,
        related_name="institution",
    )
