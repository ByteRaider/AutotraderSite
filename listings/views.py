from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden, JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import localtime
from .models import Listing, ListingImage, Message, SavedListing, ListingLike, Thread
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
    listing = get_object_or_404(Listing, pk=id)
    likes_count = listing.likes.count()
    return render(request, 'listings/listing_detail.html', {'listing': listing,
                                                            'likes_count': likes_count})

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
            messages.success(request, 'Listing saved successfully.')
            return redirect('listing_detail', id=listing_id,)
        else:
            messages.success(request, 'You already saved this listing.')
            return redirect('profile')  # Or wherever you want to redirect if listing is already saved
    else:
        messages.error(request, 'An error occurred while saving the listing.')
        return redirect('listing_list')  # Redirect to listing list if saving is not through POST request

def view_saved_listings(request):
    saved_listings = SavedListing.objects.select_related('listing').filter(user=request.user)
    return render(request, 'listings/saved_listings.html', {'saved_listings': saved_listings})
    
def remove_saved_listing(request, listing_id):
    SavedListing.objects.filter(user=request.user, listing_id=listing_id).delete()
    messages.success(request, 'Listing removed from saved listings.')
    return redirect('view_saved_listings')

#<- Messaging -->
def send_message(request, listing_id, receiver_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    receiver = get_object_or_404(User, pk=receiver_id)

    # Define form variable outside of the POST request check
    # This ensures 'form' is always defined when reaching the render function
    form = MessageForm(request.POST or None)  # Initialize form for GET and POST

    if request.method == 'POST' and form.is_valid():
        # Fetch or create the Thread
        thread, created = Thread.objects.get_or_create(
            listing=listing,
            initiator=request.user,  # Assuming the sender is always the initiator
            receiver=receiver,
            defaults={'listing': listing, 'initiator': request.user, 'receiver': receiver}
        )
        
        # Save the message with the thread
        message = form.save(commit=False)
        message.sender = request.user
        message.receiver = receiver  # Ensure this matches your model's fields
        message.thread = thread
        message.save()
        
        messages.success(request, 'Message sent successfully.')
        return redirect('messages')  # Adjust as needed

    # For GET requests or if form is not valid, show the form
    return render(request, 'listings/send_message.html', {'form': form, 'listing': listing, 'receiver': receiver})

def view_threads(request):
    # Fetch threads involving the current user, either as initiator or receiver
    threads = Thread.objects.filter(Q(initiator=request.user) | Q(receiver=request.user)).distinct().order_by('-id')
    
    # Implement pagination
    paginator = Paginator(threads, 10)  # Show 10 threads per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'listings/view_messages.html', {'page_obj': page_obj})


def view_messages(request):
    # Fetch threads involving the current user, either as initiator or receiver
    threads = Thread.objects.prefetch_related('listing', 'initiator', 'receiver').filter(Q(initiator=request.user) | Q(receiver=request.user)).distinct().order_by('-id')
    # Implement pagination
    paginator = Paginator(threads, 10)  # Show 10 threads per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'listings/view_messages.html', {'page_obj': page_obj})

@csrf_exempt  # Note: It's better to handle CSRF tokens correctly in AJAX requests rather than disabling them.
def reply_to_message(request, message_id):
    # Check for X-Requested-With header to identify AJAX requests
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        content = request.POST.get('content')
        parent_message = get_object_or_404(Message, id=message_id)
        #get thread id object
        thread_id = parent_message.thread.id
        reply = Message.objects.create(
            sender=request.user,
            receiver=parent_message.sender if request.user != parent_message.sender else parent_message.receiver,
            content=content,
            parent=parent_message,
            thread_id=thread_id
        )
        # Format the creation timestamp
        formatted_timestamp = localtime(reply.created_at).strftime('%Y-%m-%d %H:%M:%S')
        return JsonResponse({
            'message': 'Reply was successfully added.',
            'sender': reply.sender.username,
            'content': reply.content,
            'created_at': formatted_timestamp
        })
    
    # If not AJAX, or not POST, return a bad request response
    return HttpResponseBadRequest('Invalid request')

def view_message_thread(request, message_id):
    # Retrieve the main message
    main_message = get_object_or_404(Message, id=message_id)
    if request.user != main_message.sender and request.user != main_message.receiver:
        return HttpResponseForbidden("Oops! Looks like you should not be arround here.")
      # Redirect to listing list if user is not the sender or receiver
    #mark as read
    Message.objects.filter(thread=main_message.thread, receiver=request.user, is_read=False).update(is_read=True)
    # Retrieve replies to the main message
    replies = main_message.replies.all().order_by('created_at')
    
    return render(request, 'listings/message_thread.html', {
        'main_message': main_message,
        'replies': replies,
    })

def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if request.user == message.sender or request.user == message.receiver:
        message.delete()
        messages.success(request, "Message deleted successfully.")
        return redirect('messages')  # Adjust the redirect as needed
    else:
        messages.error(request, "You do not have permission to delete this message.")
        return redirect('view_message_thread', message_id=message_id)

# <!  LIKEs -->

def like_listing(request, listing_id):
    listing, created = ListingLike.objects.get_or_create(user=request.user, listing_id=listing_id)
    if created:
        messages.success(request, ' Like!')
    else:
        messages.info(request, "You've already liked this listing before.")
    return redirect('listing_detail', id=listing_id)

# Profile
def profile(request):
    user = request.user
    listings = Listing.objects.filter(seller=user)
    saved_listings = SavedListing.objects.filter(user=user)


    return render(request, 'listings/profile.html', {'user': user, 'listings': listings})