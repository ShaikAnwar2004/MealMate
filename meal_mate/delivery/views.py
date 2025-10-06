from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from delivery.models import Customer, Restaurant, MenuItem, Cart, CartItem
from django.contrib import messages  # To display messages to the user

from django.conf import settings

import razorpay
# Home Page
def index(request):
    return render(request, 'index.html')

# Sign In Page
def signin(request):
    return render(request, 'signin.html')

# Sign Up Page
def signup(request):
    return render(request, 'signup.html')

# Handle Login
def handle_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Handle admin login separately
        if username == 'admin' and password == 'admin':
            return render(request, 'admin_home.html')

        try:
            # Check if the customer exists
            Customer.objects.get(username=username, password=password)
            restaurants = Restaurant.objects.all()
            return render(request, 'customer_home.html', {
                "restaurants": restaurants,
                "username": username
            })

        except Customer.DoesNotExist:
            return render(request, 'fail.html')

    return HttpResponse("Invalid request")

# Customer Home (direct route)
def customer_home(request, username):
    restaurants = Restaurant.objects.all()
    return render(request, 'customer_home.html', {
        "restaurants": restaurants,
        "username": username
    })

# Handle Sign Up
def handle_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')

        # Check for duplicate username
        if not Customer.objects.filter(username=username).exists():
            Customer.objects.create(
                username=username,
                password=password,
                email=email,
                mobile=mobile,
                address=address
            )
            return render(request, 'signin.html')

    return HttpResponse("Invalid request")

# Add Restaurant Page
def add_restaurant_page(request):
    return render(request, 'add_restaurant.html')

# Add Restaurant
def add_restaurant(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        picture = request.POST.get('picture')
        cuisine = request.POST.get('cuisine')
        rating = request.POST.get('rating')

        Restaurant.objects.create(name=name, picture=picture, cuisine=cuisine, rating=rating)

        restaurants = Restaurant.objects.all()
        return render(request, 'show_restaurants.html', {"restaurants": restaurants})

    return HttpResponse("Invalid request")

# Show Restaurants
def show_restaurant_page(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'show_restaurants.html', {"restaurants": restaurants})

# Restaurant Menu
def restaurant_menu(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        is_veg = request.POST.get('is_veg') == 'on'
        picture = request.POST.get('picture')

        MenuItem.objects.create(
            restaurant=restaurant,
            name=name,
            description=description,
            price=price,
            is_veg=is_veg,
            picture=picture
        )
        return redirect('restaurant_menu', restaurant_id=restaurant.id)

    menu_items = restaurant.menu_items.all()
    return render(request, 'menu.html', {
        'restaurant': restaurant,
        'menu_items': menu_items,
    })

# Update Restaurant Page
def update_restaurant_page(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    return render(request, 'update_restaurant_page.html', {"restaurant": restaurant})

# Update Restaurant
def update_restaurant(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    if request.method == 'POST':
        restaurant.name = request.POST.get('name')
        restaurant.picture = request.POST.get('picture')
        restaurant.cuisine = request.POST.get('cuisine')
        restaurant.rating = request.POST.get('rating')
        restaurant.save()

        restaurants = Restaurant.objects.all()
        return render(request, 'show_restaurants.html', {"restaurants": restaurants})

# Delete Restaurant
def delete_restaurant(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    restaurant.delete()

    restaurants = Restaurant.objects.all()
    return render(request, 'show_restaurants.html', {"restaurants": restaurants})


# Update Menu item Page
def update_menuItem_page(request, menuItem_id):
    menuItem = get_object_or_404(MenuItem, id=menuItem_id)
    return render(request, 'update_menuitem_page.html', {"item": menuItem})

# Update MenuItem
def update_menuItem(request, menuItem_id):
    menuItem = get_object_or_404(MenuItem, id=menuItem_id)

    if request.method == 'POST':
        menuItem.name = request.POST.get('name')
        menuItem.description = request.POST.get('description')
        menuItem.price = request.POST.get('price')
        menuItem.is_veg = request.POST.get('is_veg') == 'on'
        menuItem.picture = request.POST.get('picture')

        menuItem.save()

        restaurants = Restaurant.objects.all()
        return render(request, 'show_restaurants.html', {"restaurants": restaurants})

# Delete menuItem
def delete_menuItem(request, menuItem_id):
    menuItem = get_object_or_404(MenuItem, id=menuItem_id)
    menuItem.delete()

    restaurants = Restaurant.objects.all()
    return render(request, 'show_restaurants.html', {"restaurants": restaurants})


# Customer Menu
def customer_menu(request, restaurant_id, username):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    menu_items = restaurant.menu_items.all()
    return render(request, 'customer_menu.html', {
        'restaurant': restaurant,
        'menu_items': menu_items,
        'username':username
    })

# Add items to cart
def add_to_cart(request, item_id, username):
    customer = get_object_or_404(Customer, username=username)
    item = get_object_or_404(MenuItem, id=item_id)
    cart, _ = Cart.objects.get_or_create(customer=customer)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, menu_item=item)
    if not created:
        cart_item.quantity += 1
    cart_item.save()

    messages.success(request, f"{item.name} added to your cart!")
    return redirect('customer_menu', restaurant_id=item.restaurant.id, username=username)


# Show Cart
def show_cart_page(request, username):
    customer = get_object_or_404(Customer, username=username)
    cart = Cart.objects.filter(customer=customer).first()
    cart_items = cart.cart_items.select_related('menu_item') if cart else []
    total_price = cart.total_price() if cart else 0

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'username': username,
    })


def update_quantity(request, item_id, username, action):
    customer = get_object_or_404(Customer, username=username)
    cart = Cart.objects.filter(customer=customer).first()
    if not cart:
        return redirect('show_cart_page', username=username)

    cart_item = get_object_or_404(CartItem, cart=cart, menu_item_id=item_id)
    if action == 'inc':
        cart_item.quantity += 1
        cart_item.save()
    elif action == 'dec':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

    return redirect('show_cart_page', username=username)



# Checkout View
def checkout(request, username):
    # Fetch customer and their cart
    customer = get_object_or_404(Customer, username=username)
    cart = Cart.objects.filter(customer=customer).first()
    cart_items = cart.cart_items.select_related('menu_item') if cart else []
    total_price = cart.total_price() if cart else 0

    if total_price == 0:
        return render(request, 'checkout.html', {
            'username': username,
            'error': 'Your cart is empty!',
        })

    # Validate Razorpay keys
    key_id = getattr(settings, 'RAZORPAY_KEY_ID', None)
    key_secret = getattr(settings, 'RAZORPAY_KEY_SECRET', None)
    if not key_id or not key_secret:
        return render(request, 'checkout.html', {
            'username': username,
            'cart_items': cart_items,
            'total_price': total_price,
            
        })

    # Initialize Razorpay client
    client = razorpay.Client(auth=(key_id, key_secret))

    # Create Razorpay order
    try:
        order_data = {
            'amount': int(total_price * 100),  # Amount in paisa
            'currency': 'INR',
            'payment_capture': '1',
        }
        order = client.order.create(data=order_data)
        order_id = order['id']
    except Exception as e:
        # Attempt to pull more details from Razorpay error response if present
        error_message = str(e)
        try:
            if isinstance(e.args[0], dict):
                err = e.args[0].get('error') or {}
                desc = err.get('description')
                code = err.get('code')
                error_message = f"{code or 'ERROR'}: {desc or error_message}"
        except Exception:
            pass

        # Log server-side for debugging
        print('Razorpay order.create failed:', e)

        return render(request, 'checkout.html', {
            'username': username,
            'cart_items': cart_items,
            'total_price': total_price,
            'error': f'Payment gateway error: {error_message}',
        })

    # Pass the order details to the frontend
    return render(request, 'checkout.html', {
        'username': username,
        'cart_items': cart_items,
        'total_price': total_price,
        'razorpay_key_id': key_id,
        'order_id': order_id,
        'amount': total_price,
    })



# Orders Page
def orders(request, username):
    customer = get_object_or_404(Customer, username=username)
    cart = Cart.objects.filter(customer=customer).first()

    cart_items = cart.cart_items.select_related('menu_item') if cart else []
    total_price = cart.total_price() if cart else 0

    if cart:
        cart.cart_items.all().delete()

    return render(request, 'orders.html', {
        'username': username,
        'customer': customer,
        'cart_items': cart_items,
        'total_price': total_price,
    })

