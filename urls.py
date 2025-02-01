
from django.urls import path,include
from furniclove_app import views
from django.contrib.auth import views as auth_views
from django.contrib import admin
#from .views import product_detail_with_variant

urlpatterns = [
    path('', views.index, name='index'),
    path('shop/', views.shop, name='shop'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('cart/', views.cart, name='cart'),
    path('wishlist/', views.wishlist, name='wishlist'),


    path('signup/', views.signup_view, name='signup'),
    path('otp/', views.otp_view, name='otp'),
    path('resend_otp/', views.resend_otp, name='resend_otp'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('checkout/', views.checkout_view, name='checkout'),
    path('profile/', views.profile_view, name='profile'),

   path('product/<int:product_id>/', views.product_detail, name='product_detail'),

   path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),

  path('product/<int:product_id>/variant/<int:variant_id>/', views.product_detail, name='product_detail_with_variant'),  # Product with variant

  path('place-order/', views.place_order, name='place_order'),
  path('order-history/', views.order_history, name='order_history'),
  path('order/<int:order_id>/', views.order_detail, name='order_detail'),

   
]




   
    
