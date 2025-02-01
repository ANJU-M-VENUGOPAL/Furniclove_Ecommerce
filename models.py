from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)  
    description = models.TextField(default="No description available.")  
    original_price = models.DecimalField(max_digits=10, decimal_places=2)  
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True) 
    discount_percent = models.IntegerField()  
    image = models.ImageField(upload_to='product_images/') 
    thumbnail_1 = models.ImageField(upload_to='product_images/', blank=True, null=True)
    thumbnail_2 = models.ImageField(upload_to='product_images/', blank=True, null=True)
    thumbnail_3 = models.ImageField(upload_to='product_images/', blank=True, null=True)
    thumbnail_4 = models.ImageField(upload_to='product_images/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    stock = models.PositiveIntegerField(default=0) 
   

    def save(self, *args, **kwargs):
        # Validate discount_percent
        if self.discount_percent < 0 or self.discount_percent > 100:
            raise ValueError("Discount percent must be between 0 and 100.")
        
        # Calculate discount_price based on discount_percent and original_price
        if self.discount_percent and self.original_price:
            self.discount_price = self.original_price - (self.original_price * self.discount_percent / 100)
        super(Product, self).save(*args, **kwargs)


class ColorVariant(models.Model):
    product = models.ForeignKey(Product, related_name='color_variants', on_delete=models.CASCADE)
    color_name = models.CharField(max_length=50)  
    color_code = models.CharField(max_length=7)  
    main_image = models.ImageField(upload_to='variant_images/')  
    thumbnail_1 = models.ImageField(upload_to='variant_images/', blank=True, null=True)
    thumbnail_2 = models.ImageField(upload_to='variant_images/', blank=True, null=True)
    thumbnail_3 = models.ImageField(upload_to='variant_images/', blank=True, null=True)
    thumbnail_4 = models.ImageField(upload_to='variant_images/', blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)  
    price_override = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True,
        help_text="If different from the product's original price"
    )

    def save(self, *args, **kwargs):
        if self.price_override:
            # Calculate discount for the variant if price_override is provided
            self.discount_price = self.price_override - (self.price_override * self.product.discount_percent / 100)
        else:
            # If no price_override, calculate using the product's original price and discount percent
            self.discount_price = self.product.original_price - (self.product.original_price * self.product.discount_percent / 100)

       
        if self.discount_price < 0:
            self.discount_price = 0  
        
        super(ColorVariant, self).save(*args, **kwargs)


class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid'),
    ]
    
    customer = models.ForeignKey(User, on_delete=models.CASCADE)  # Linking to the User model
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='unpaid')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)  # Total order price
    shipping_address = models.TextField()
    shipping_method = models.CharField(max_length=100)
    tracking_number = models.CharField(max_length=50, blank=True, null=True)  # For shipped orders
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} by {self.customer.username}"



class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)  # Reference to the Order
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Product being purchased
    quantity = models.PositiveIntegerField(default=1)  # Quantity of the product ordered
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price at the time of order (may be discounted)
    
    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"
