from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('accounts/profile/', views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='listings/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='listings/logout.html'), name='logout'),
    path('register/', views.register, name='register'),
    path('', views.listing_list, name='listing_list'),
    path('listings/', views.listing_list, name='listing_list'),
    path('listings/add/', views.add_listing, name='add_listing'),
    path('listings/<int:id>/', views.listing_detail, name='listing_detail'),
    path('listings/<int:listing_id>/save/', views.save_listing, name='save_listing'),
    path('listings/<int:listing_id>/remove_saved/', views.remove_saved_listing, name='remove_saved_listing'),
    path('listings/<int:listing_id>/like/', views.like_listing, name='like_listing'),
    path('messages/send/<int:listing_id>/<int:receiver_id>/', views.send_message, name='send_message'),
    path('messages/', views.view_messages, name='view_messages'),
]


