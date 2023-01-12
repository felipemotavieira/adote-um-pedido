from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class User(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    email = models.EmailField(max_length=50, unique=True)
    cpf = models.CharField(max_length=11, unique=True)

    address = models.OneToOneField(
        "addresses.Address",
        on_delete=models.CASCADE,
        related_name="user",
        null=True,
    )
