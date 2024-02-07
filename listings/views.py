from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, ListingForm
from .models import Listing

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')  # Assuming you have a URL named 'login'
    else:
        form = UserRegisterForm()
    return render(request, 'listings/register.html', {'form': form})

def listing_list(request):
    listings = Listing.objects.all()
    return render(request, 'listings/listing_list.html', {'listings': listings})

def listing_detail(request, id):
    listing = Listing.objects.get(id=id)
    return render(request, 'listings/listing_detail.html', {'listing': listing})

def add_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.seller = request.user
            listing.save()
            return redirect('listing_list')
    else:
        form = ListingForm()
    return render(request, 'listings/add_listing.html', {'form': form})
