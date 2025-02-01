from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm
from django.contrib import messages
from django.conf import settings
from django.utils import timezone
from django.http import JsonResponse
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
import random
from datetime import timedelta
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from .forms import SignupForm
from django.shortcuts import get_object_or_404
from django.http import HttpResponse


from django.core.paginator import Paginator
from admin_panel.models import Product,ColorVariant,Order, OrderItem,Category



# Views for different pages
def index(request):
    return render(request, 'index.html')

    

def shop(request):
    category_filter = request.GET.get('category', '')
    sort_by = request.GET.get('sort-by', '')

    products = Product.objects.all()

    # Apply category filter if provided
    if category_filter:
        products = products.filter(category__name=category_filter)

    # Apply sorting
    if sort_by == 'a-to-z':
        products = products.order_by('name')
    elif sort_by == 'z-to-a':
        products = products.order_by('-name')
    elif sort_by == 'price-low-to-high':
        products = products.order_by('original_price')
    elif sort_by == 'price-high-to-low':
        products = products.order_by('-original_price')
    elif sort_by == 'discount-low-to-high':
        products = products.order_by('discount_percent')
    elif sort_by == 'discount-high-to-low':
        products = products.order_by('-discount_percent')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')

    categories = Category.objects.all()  # For displaying categories in the filter dropdown

    # Pagination 
    paginator = Paginator(products, 6)  # 6 products per page
    page_number = request.GET.get('page', 1)  # Get the current page number from the query parameters
    page_obj = paginator.get_page(page_number)  # Get the page object

    return render(request, 'shop.html', {
        'page_obj': page_obj,  # Pass page_obj for pagination
        'categories': categories,
        'category': category_filter,
        'sort_by': sort_by
    })
    

    
    return render(request, 'shop.html', {
        'products': page_obj.object_list,
        'page_obj': page_obj,
        #'category': category,
       #'sort_by': sort_by,
    })


def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'services.html')

def contact(request):
    return render(request, 'contact.html')

@login_required(login_url='login')
def cart(request):
    # Your logic for the cart
    return render(request, 'cart.html')

@login_required
def profile_view(request):
    user = request.user  # Get the logged-in user object
    return render(request, 'profile.html', {'user': user})

def otp_view(request):
    if request.method == 'POST':
        otp_input = request.POST.get('otp')
        otp_code = request.session.get('otp_code')
        email = request.session.get('otp_email')

        if otp_input == otp_code:
            messages.success(request, "OTP verified successfully!")
            return redirect('login')  # Redirect to the login page after OTP verification
        else:
            messages.error(request, "Invalid OTP. Please try again.")

    return render(request, 'otp.html')  # Render OTP input page


# Send OTP function
def send_otp(request, user):
    otp = random.randint(100000, 999999)  # Generate a random 6-digit OTP
    
    # Send OTP via email
    subject = "Your OTP for Signup"
    message = f"Your OTP is {otp}."
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])
    
    # Store OTP in session for later verification
    request.session['otp_code'] = str(otp)
    request.session['otp_email'] = user.email  # Store email in session for later verification


def resend_otp(request):
    # Get the user email from the session
    email = request.session.get('otp_email')
    user = User.objects.get(email=email)
    
    # Resend OTP
    send_otp(request, user)
    
    messages.success(request, "OTP resent to your email.")
    return redirect('otp')  # Redirect back to the OTP page



def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # Create the user
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

            # Send OTP to the user's email
            send_otp(request, user)

            messages.success(request, "You have successfully signed up. Please check your email for the OTP.")
            return redirect('otp')  # Redirect to the OTP verification page
        else:
            error = form.errors.as_text()  # Collect errors
            return render(request, 'signup.html', {'form': form, 'error': error})

    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Authenticate the user
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, "Login successful!")
                return redirect('index')  # Redirect to the index page after login
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid credentials. Please try again.")
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

    
# Logout View
@login_required
def logout_view(request):
    logout(request)  # Logs out the user
    messages.success(request, "You have successfully logged out.")
    return redirect('login')  # Redirect to the login page
  

def checkout_view(request):
    return render(request, 'checkout.html')


def wishlist(request):
    # Logic to handle the wishlist (e.g., fetching wishlist items)
    return render(request, 'wishlist.html', {})


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    return redirect('cart')  



def product_detail(request, product_id, variant_id=None):
    product = get_object_or_404(Product, id=product_id)
    color_variants = product.color_variants.all()
    selected_variant = None

    if variant_id:
        selected_variant = get_object_or_404(ColorVariant, id=variant_id, product=product)

    # Calculate discount percentage and price for the selected variant
    discount_percent_variant = product.discount_percent  # Use product's discount percent for the variant
    discount_price_variant = 0
    if selected_variant:
        if selected_variant.price_override:
            # Use the price_override of the variant as the new original price for the variant
            original_price_variant = selected_variant.price_override
            # Calculate discount price using the product's discount_percent for the variant
            discount_price_variant = original_price_variant - (original_price_variant * product.discount_percent / 100)
        else:
            # If no price_override, use the product's original price and discount_percent
            discount_price_variant = product.original_price - (product.original_price * product.discount_percent / 100)

    # Calculate discount percentage and price for the product
    discount_percent_product = 0
    if product.original_price > product.discount_price:
        discount_price_product = product.original_price - product.discount_price
        if product.original_price > 0:
            discount_percent_product = (discount_price_product / product.original_price) * 100

    return render(request, 'product_detail.html', {
        'product': product,
        'color_variants': color_variants,
        'selected_variant': selected_variant,
        'discount_price_variant': discount_price_variant,
        'discount_percent_variant': discount_percent_variant,
        'discount_percent_product': discount_percent_product,
        'category': product.category,
    })


# Place order
@login_required
def place_order(request):
    cart_items = get_cart_items(request)  # Function to get cart items (assumed from session or cart model)
    if request.method == 'POST':
        order = Order.objects.create(
            customer=request.user,
            total_amount=calculate_total(cart_items),  # Custom function to calculate total order price
            shipping_address=request.POST['shipping_address'],
            shipping_method=request.POST['shipping_method'],
        )
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price=item['price'],
            )
        clear_cart(request)  # Clear the cart after order is placed
        return redirect('order_success')  # Redirect to a success page
    return render(request, 'checkout.html', {'cart_items': cart_items})


# View order history
@login_required
def order_history(request):
    orders = Order.objects.filter(customer=request.user).order_by('-created_at')
    return render(request, 'order_history.html', {'orders': orders})


# View order details
@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order=order)
    return render(request, 'order_detail.html', {'order': order, 'order_items': order_items})