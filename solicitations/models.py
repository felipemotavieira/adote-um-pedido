from django.db import models

class StatusChoices(models.TextChoices):
    DISPONIVEL = "Disponível"
    NAO_DISPONIVEL = "Não disponível"
    ENVIADO = "Enviado"
    RECEBIDO = "Recebido"
    NOT_INFORMED = "Não informado"

class Solicitation(models.Model):
    description = models.CharField(max_length=255)
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
