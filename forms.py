from django import forms
from .models import Product, ColorVariant,Order

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description',  'original_price', 'discount_price', 'stock', 'image', 'thumbnail_1', 'thumbnail_2', 'thumbnail_3', 'thumbnail_4']

class ColorVariantForm(forms.ModelForm):
    class Meta:
        model = ColorVariant
        fields = ['color_name', 'color_code', 'main_image', 'thumbnail_1', 'thumbnail_2', 'thumbnail_3', 'thumbnail_4', 'stock', 'price_override']

'''
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']   
'''            

class OrderEditForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['order_status', 'payment_status']
