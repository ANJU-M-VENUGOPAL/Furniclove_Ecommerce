from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', views.admin_login, name='admin_login'),
    path('admin_home/', views.admin_home, name='admin_home'),
    path('admin_logout/', views.admin_logout, name='admin_logout'), 


    path('user_management/', views.user_management, name='user_management'),   
    path('block-user/<int:user_id>/', views.block_user, name='block_user'),
    path('activate-user/<int:user_id>/', views.activate_user, name='activate_user'),

    path('product-management/', views.product_management, name='product_management'),
    path('add-product/', views.add_product, name='add_product'),
    path('edit-product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete-product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('view-product/<int:product_id>/', views.view_product, name='view_product'),


    path('product/<int:product_id>/variants/', views.variant_management, name='variant_management'),
    path('product/<int:product_id>/add_variant/', views.add_variant, name='add_variant'),
    path('variant/<int:variant_id>/edit/', views.edit_variant, name='edit_variant'),
    path('variant/<int:variant_id>/delete/', views.delete_variant, name='delete_variant'),

    path('category_management/', views.category_management, name='category_management'),
    path('add_category/', views.add_category, name='add_category'),
    path('edit_category/<int:category_id>/', views.edit_category, name='edit_category'),
    path('delete_category/<int:category_id>/', views.delete_category, name='delete_category'),

    path('order_management/', views.order_management, name='order_management'),  
    path('admin/orders/', views.order_management, name='order_management'),
    path('admin/order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('admin/order/edit/<int:order_id>/', views.order_edit, name='order_edit'),
]    