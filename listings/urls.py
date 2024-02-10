from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('accounts/profile/', views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='listings/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='listings/profile.html'), name='logout'),
    path('register/', views.register, name='register'),
    
    path('', views.listing_list, name='listing_list'),
    path('listings/', views.listing_list, name='listing_list'),
    path('listings/add/', views.add_listing, name='add_listing'),
    path('listings/<int:id>/', views.listing_detail, name='listing_detail'),

    path('listings/<int:listing_id>/save/', views.save_listing, name='save_listing'),
    path('view_saved_listings/', views.view_saved_listings, name='view_saved_listings'),
    path('listings/<int:listing_id>/remove_saved/', views.remove_saved_listing, name='remove_saved_listing'),
    path('listings/<int:listing_id>/like/', views.like_listing, name='like_listing'),
    
    path('messages/send/<int:listing_id>/<int:receiver_id>/', views.send_message, name='send_message'),
    path('messages/', views.view_messages, name='messages'),
    path('messages/reply/<int:message_id>/', views.reply_to_message, name='reply_to_message'),
    path('messages/delete/<int:message_id>/', views.delete_message, name='delete_message'),
    path('messages/thread/<int:message_id>/', views.view_message_thread, name='view_message_thread'),
]



