from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Listing

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['seller','make', 'model', 'year', 'mileage', 'condition', 'description', 'price', 'VIN']
        # Include other fields as necessary