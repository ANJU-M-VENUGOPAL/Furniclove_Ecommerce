from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Product, ColorVariant,Order,Category
from .forms import ProductForm, ColorVariantForm,OrderEditForm




def admin_login(request):
    if request.user.is_authenticated:
        return redirect('admin_home')  # Redirect to admin home if logged in already

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_superuser:  # Ensure the user is a superuser
                login(request, user)
                return redirect('admin_home')  # Redirect to admin home after successful login
            else:
                # Show an error message if the user is not an admin
                messages.error(request, "You are not authorized to access this page.")
                return redirect('admin_login')  # Redirect to login page again if not authorized
    else:
        form = AuthenticationForm()

    return render(request, 'admin_login.html', {'form': form})
    

@login_required
def admin_home(request):
    # Restrict access to only superusers
    if not request.user.is_superuser:
        return redirect('admin_login')  # Redirect to login if not a superuser
    return render(request, 'admin_home.html')




# User Management
@login_required
def user_management(request):
    if not request.user.is_superuser:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')  # Redirect to home or another page if not admin

    users = User.objects.exclude(is_superuser=True)  # Exclude superuser from the list
    return render(request, 'user_management.html', {'users': users})

# Block a user (deactivate)
@login_required
def block_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.user.is_superuser:
        if user.is_superuser:
            messages.error(request, 'You cannot block the superuser.')
        else:
            user.is_active = False
            user.save()
            messages.success(request, f'{user.username} has been blocked successfully.')
    else:
        messages.error(request, 'You do not have permission to block users.')
    return redirect('user_management')

# Activate a user (reactivate)
@login_required
def activate_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.user.is_superuser:
        if user.is_superuser:
            messages.error(request, 'You cannot activate the superuser.')
        else:
            user.is_active = True
            user.save()
            messages.success(request, f'{user.username} has been activated successfully.')
    else:
        messages.error(request, 'You do not have permission to activate users.')
    return redirect('user_management')



# Product Management
@login_required
def product_management(request):
    products = Product.objects.all()

    # Create a list of thumbnail fields for each product
    for product in products:
        product.thumbnails = [
            product.thumbnail_1,
            product.thumbnail_2,
            product.thumbnail_3,
            product.thumbnail_4,
        ]

    context = {
        'products': products
    }
    return render(request, 'product_management.html', context)


# add product
def add_product(request):
    if request.method == "POST":
        # Retrieve form data
        name = request.POST.get("name")
        description = request.POST.get("description")
        category = request.POST.get("category")
        original_price = request.POST.get("original_price")
        discount_percent = request.POST.get("discount_percent", 0)  # Default to 0 if not provided
        stock = request.POST.get("stock")
        image = request.FILES.get("image")
        thumbnail_1 = request.FILES.get("thumbnail_1")
        thumbnail_2 = request.FILES.get("thumbnail_2")
        thumbnail_3 = request.FILES.get("thumbnail_3")
        thumbnail_4 = request.FILES.get("thumbnail_4")

        # Validation checks
        if not name or not description or not category or not original_price or not stock or not image:
            return HttpResponse("All required fields must be filled.", status=400)

        try:
            original_price = float(original_price)
            discount_percent = float(discount_percent) if discount_percent else 0
            stock = int(stock)

            if original_price < 0 or discount_percent < 0 or stock < 0:
                return HttpResponse("Prices, discount, and stock values must be non-negative.", status=400)

        except ValueError:
            return HttpResponse("Invalid numeric values.", status=400)

        # Save product to the database
        product = Product(
            name=name,
            description=description,
            category=category,
            original_price=original_price,
            discount_percent=discount_percent,
            stock=stock,
            image=image,
            thumbnail_1=thumbnail_1,
            thumbnail_2=thumbnail_2,
            thumbnail_3=thumbnail_3,
            thumbnail_4=thumbnail_4,
        )
        product.save()
        return redirect("product_management")  # Redirect to product management page

    # Render the form page for GET requests
    return render(request, "add_product.html")



# view a product
def view_product(request, product_id):
    product = Product.objects.get(id=product_id)
    
    
    thumbnails = []
    for i in range(1, 5):
        thumbnail_field = getattr(product, f'thumbnail_{i}', None)
        if thumbnail_field:
            thumbnails.append(thumbnail_field.url)

    return render(request, 'view_product.html', {'product': product, 'thumbnails': thumbnails})    


# edit  product
def edit_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        product.category = request.POST.get('category')
        product.original_price = request.POST.get('original_price')
        product.discount_percent = int(request.POST.get('discount_percent'))  
        product.stock = request.POST.get('stock')

        # Handle image and thumbnails 
        if 'image' in request.FILES:
            product.image = request.FILES['image']
        if 'thumbnail_1' in request.FILES:
            product.thumbnail_1 = request.FILES['thumbnail_1']
        if 'thumbnail_2' in request.FILES:
            product.thumbnail_2 = request.FILES['thumbnail_2']
        if 'thumbnail_3' in request.FILES:
            product.thumbnail_3 = request.FILES['thumbnail_3']
        if 'thumbnail_4' in request.FILES:
            product.thumbnail_4 = request.FILES['thumbnail_4']

        
        product.save()  

        return redirect('product_management')  

    return render(request, 'edit_product.html', {'product': product})


# delete a product
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('product_management')



# variant list
def variant_management(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    color_variants = ColorVariant.objects.filter(product=product)
    return render(request, 'variant_management.html', {'product': product, 'color_variants': color_variants})


# add variant
def add_variant(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        form = ColorVariantForm(request.POST, request.FILES)
        if form.is_valid():
            variant = form.save(commit=False)
            variant.product = product  
            variant.save()
            return redirect('view_product', product.id)  
    else:
        form = ColorVariantForm()

    return render(request, 'add_variant.html', {'form': form, 'product': product})


# edit variant
def edit_variant(request, variant_id):
    
    variant = get_object_or_404(ColorVariant, id=variant_id)
    product = variant.product  

    if request.method == 'POST':
        
        form = ColorVariantForm(request.POST, request.FILES, instance=variant)
        if form.is_valid():
            form.save()  
            return redirect('variant_management', product.id)  
    else:
        form = ColorVariantForm(instance=variant)

    return render(request, 'edit_variant.html', {
        'form': form,
        'product': product,
    })


# delete variant
def delete_variant(request, variant_id):
    variant = get_object_or_404(Variant, id=variant_id)
    product_id = variant.product.id
    variant.delete()
    return redirect('product_variant_list', product_id=product_id)


# Category Management
@login_required
def category_management(request):
    if not request.user.is_superuser:
        messages.error(request, "You do not have permission to access this page.")
        return redirect('admin_home')

    categories = Category.objects.all()
    return render(request, 'category_management.html', {'categories': categories})

# add category
@login_required
def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')

        if not name:
            messages.error(request, "Category name is required.")
            return redirect('add_category')  # Redirect if validation fails

        category = Category(name=name, description=description)
        category.save()
        messages.success(request, "Category added successfully.")
        return redirect('category_management')

    return render(request, 'add_category.html')


# edit category
@login_required
def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if request.method == 'POST':
        category.name = request.POST.get('name')
        category.description = request.POST.get('description')
        category.save()
        messages.success(request, "Category updated successfully.")
        return redirect('category_management')

    return render(request, 'edit_category.html', {'category': category})


# delete category
@login_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    messages.success(request, "Category deleted successfully.")
    return redirect('category_management')



# Order Management
@login_required
def order_management(request):
    if not request.user.is_superuser:
        return redirect('admin_login')  

    orders = Order.objects.all()  # Fetch all orders
    return render(request, 'order_management.html', {'orders': orders})


# View specific order's details
@login_required
def order_detail(request, order_id):
    if not request.user.is_superuser:
        return redirect('admin_login')
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order_detail.html', {'order': order})
    

# edit order details 
@login_required
def order_edit(request, order_id):
    if not request.user.is_superuser:
        return redirect('admin_login')
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        form = OrderEditForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('order_management')
    else:
        form = OrderEditForm(instance=order)

    return render(request, 'order_edit.html', {'form': form, 'order': order})




# Log out
def admin_logout(request):
    logout(request)
    return redirect('admin_login')  # Redirect to login page after logout
