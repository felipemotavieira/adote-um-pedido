from django.db import models

class TypeChoice(models.TextChoices):
    ORFANATO = "Orfanato"
    ASILO = "Asilo"
    NOT_INFORMED = "Não informado"

class Institution(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
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

