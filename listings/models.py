from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} Profile'

# listings
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
    
class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='listing_images/')
    
    def __str__(self):
        return f'Image for {self.listing.make} {self.listing.model} - {self.listing.year}'

class SavedListing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'listing')
    def __str__(self):
        return f'{self.user.username} saved {self.listing}'    
    
# LIKES
class ListingLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'listing')


#  Messaging  -- Maybe create app later?
class Thread(models.Model):
    listing = models.ForeignKey(Listing, related_name='threads', on_delete=models.CASCADE)
    initiator = models.ForeignKey(User, related_name='initiated_threads', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_threads', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('listing', 'initiator', 'receiver')

    def __str__(self):
        return f"{self.listing} | {self.initiator} -> {self.receiver}"

class Message(models.Model):
    listing = models.ForeignKey('Listing', on_delete=models.CASCADE, null=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread, related_name='messages', on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        return f'Message from {self.sender} to {self.receiver} - {self.created_at}'

