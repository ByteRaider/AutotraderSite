from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from .models import Profile, Listing, ListingImage, Message, SavedListing, ListingLike
from .forms import UserRegisterForm, ListingForm, ListingImageForm, MessageForm

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
    listing = Listing.objects.get(pk=id)
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

def save_listing(request, listing_id):
    if request.method == 'POST':
        listing = Listing.objects.get(pk=listing_id)
        saved_listing, created = SavedListing.objects.get_or_create(user=request.user, listing=listing)
        if created:
            return redirect('listing_detail', listing_id=listing_id)
        else:
            return redirect('listing_list')  # Or wherever you want to redirect if listing is already saved
    else:
        return redirect('listing_list')  # Redirect to listing list if saving is not through POST request

def view_saved_listings(request):
    saved_listings = SavedListing.objects.filter(user=request.user)
    return render(request, 'listings/saved_listings.html', {'saved_listings': saved_listings})

def remove_saved_listing(request, listing_id):
    SavedListing.objects.filter(user=request.user, listing_id=listing_id).delete()
    messages.success(request, 'Listing removed from saved listings.')
    return redirect('view_saved_listings')

#<- Messaging -->
def send_message(request, listing_id, receiver_id):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = User.objects.get(pk=receiver_id)
            message.listing = Listing.objects.get(pk=listing_id)
            message.save()
            return redirect('messages')
    else:
        form = MessageForm()
    return render(request, 'listings/send_message.html', {'form': form})

def view_messages(request):
    message_list = Message.objects.filter(receiver=request.user).order_by('-created_at')
    paginator = Paginator(message_list, 10)  # Show 10 messages per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'listings/view_messages.html', {'page_obj': page_obj})

# <!  LIKEs -->
def like_listing(request, listing_id):
    listing, created = ListingLike.objects.get_or_create(user=request.user, listing_id=listing_id)
    if created:
        messages.success(request, 'Listing liked.')
    else:
        messages.info(request, 'You already like this listing.')
    return redirect('listing_detail', listing_id=listing_id)

# Profile
def profile(request):
    user = request.user
    listings = Listing.objects.filter(seller=user)
    view_saved_listings = SavedListing.objects.filter(user=user)


    return render(request, 'listings/profile.html', {'user': user, 'listings': listings})