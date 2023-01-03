from django.db import models

class Address(models.Model):
    state = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    number = models.IntegerField()
    district = models.CharField(max_length=255)
    zip_code = models.IntegerField()