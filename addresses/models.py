from django.db import models
import uuid

class Address(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    number = models.IntegerField()
    district = models.CharField(max_length=50)
    zip_code = models.IntegerField()