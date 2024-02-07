from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Listing(models.Model):
    seller = models.ForeignKey(User, related_name='listings', on_delete=models.CASCADE)
    make = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    year = models.IntegerField()
    mileage = models.IntegerField()
    condition = models.CharField(max_length=255)
