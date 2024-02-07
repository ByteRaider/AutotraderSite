from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from .forms import UserRegisterForm, ListingForm, ListingImageForm
from .models import Listing, ListingImage

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
    
    # Capture query parameters
    make = request.GET.get('make')
    model = request.GET.get('model')
    year = request.GET.get('year')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    # Apply filters if present
    if make:
        listings = listings.filter(make__iexact=make)
    if model:
        listings = listings.filter(model__iexact=model)
    if year:
        listings = listings.filter(year__exact=year)
    if min_price:
        listings = listings.filter(price__gte=min_price)
    if max_price:
        listings = listings.filter(price__lte=max_price)

    return render(request, 'listings/listing_list.html', {'listings': listings})


def listing_detail(request, id):
    listing = Listing.objects.get(id=id)
    return render(request, 'listings/listing_detail.html', {'listing': listing})

def add_listing(request):
    if request.method == 'POST':
        listing_form = ListingForm(request.POST, request.FILES)
        files = request.FILES.getlist('image')  # Handle multiple file uploads
        if listing_form.is_valid():
            listing = listing_form.save(commit=False)
            listing.seller = request.user
            listing.save()
            for f in files:
                ListingImage.objects.create(listing=listing, image=f)
            return redirect('listing_list')
    else:
        listing_form = ListingForm()
        image_form = ListingImageForm()
    return render(request, 'listings/add_listing.html', {'listing_form': listing_form, 'image_form': image_form})