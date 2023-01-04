from django.db import models
import uuid

class StatusChoices(models.TextChoices):
    DISPONIVEL = "Disponível"
    NAO_DISPONIVEL = "Não disponível"
    ENVIADO = "Enviado"
    RECEBIDO = "Recebido"
    NOT_INFORMED = "Não informado"

class Solicitation(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    description = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices= StatusChoices.choices, default= StatusChoices.NOT_INFORMED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="solicitations",
    )

#!!!!!!!!
    donee = models.OneToOneField(
        "donees.Donee",
        on_delete=models.CASCADE,
        related_name="solicitations",
    )
