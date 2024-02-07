from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} Profile'


class Listing(models.Model):
    seller = models.ForeignKey(User, related_name='listings', on_delete=models.CASCADE)
    make = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    year = models.IntegerField()
    mileage = models.IntegerField()
    condition = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    VIN = models.CharField(max_length=255)
    
