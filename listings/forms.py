from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Listing, ListingImage, Message 
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

class SearchForm(forms.Form):
    make = forms.CharField(required=False)
    model = forms.CharField(required=False)
    year = forms.IntegerField(required=False)
    min_price = forms.DecimalField(required=False)
    max_price = forms.DecimalField(required=False)

class ListingImageForm(forms.ModelForm):
    class Meta:
        model = ListingImage
        fields = ['image']
        #widgets = {'image': forms.ClearableFileInput(attrs={'multiple': True})}

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']

class MessageReplyForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']