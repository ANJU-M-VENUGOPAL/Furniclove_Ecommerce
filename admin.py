from django.contrib import admin
from .models import Product, ColorVariant, Order, Category, OrderItem

class ColorVariantInline(admin.TabularInline):
    model = ColorVariant
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description') 
    search_fields = ('name',) 
    ordering = ('name',)  
    list_filter = ('name',)  

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'original_price', 'discount_percent', 'discount_price', 'category', 'stock')
    inlines = [ColorVariantInline]

@admin.register(ColorVariant)
class ColorVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'color_name', 'stock', 'price_override')
    list_filter = ('color_name',)
    search_fields = ('product__name', 'color_name')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0  # Number of empty forms to display by default

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'total_amount', 'order_status', 'payment_status', 'created_at', 'updated_at')
    search_fields = ('customer__username', 'id')
    list_filter = ('order_status', 'payment_status', 'created_at')
    inlines = [OrderItemInline]  # Display the items of the order inline

    # Custom actions to mark orders as paid or shipped
    actions = ['mark_as_shipped', 'mark_as_paid']

    def mark_as_shipped(self, request, queryset):
        queryset.update(order_status='shipped')
    mark_as_shipped.short_description = "Mark selected orders as shipped"

    def mark_as_paid(self, request, queryset):
        queryset.update(payment_status='paid')
    mark_as_paid.short_description = "Mark selected orders as paid"
