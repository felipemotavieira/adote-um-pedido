from django.db import models
import uuid

class TypeChoice(models.TextChoices):
    ORFANATO = "Orfanato"
    ASILO = "Asilo"
    NOT_INFORMED = "Não informado"

class Institution(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    cnpj = models.IntegerField()
    phone = models.IntegerField()
    type = models.CharField(max_length=20, choices= TypeChoice.choices, default= TypeChoice.NOT_INFORMED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    address = models.OneToOneField(
        "addresses.Address",
        on_delete=models.CASCADE,
        related_name="institution"
    )

    user = models.OneToOneField(
        "users.User",
        on_delete=models.CASCADE,
        related_name="institution"
    )

