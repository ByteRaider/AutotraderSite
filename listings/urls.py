from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.listing_list, name='listing_list'),
    path('<int:id>/', views.listing_detail, name='listing_detail'),
    path('add/', views.add_listing, name='add_listing'),

]


