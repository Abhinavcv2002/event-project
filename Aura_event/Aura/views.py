from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import *
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.http import Http404
from django.core.paginator import Paginator
import razorpay
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal



def home(request):
    # Get all events to display on home page
    events = event.objects.all()
    return render(request, 'home.html', {'events': events})

def event_detail(request, event_id):
    # Get specific event and its products
    event_obj = get_object_or_404(event, pk=event_id)
    products = Product.objects.filter(event=event_obj)
    return render(request, 'event_details.html', {
        'event': event_obj,
        'products': products
    })
  
def event_products(request):
    return render(request, 'event.html')
  
def signin(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username') 
        password = request.POST.get('password')
            
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            request.session['username'] = username
            if user.is_superuser:
                return redirect('admin_page')
            else:
                return redirect('home')
        else:
            messages.error(request, "Invalid credentials.")
    
    return render(request, 'signin.html')

def signup(request):
    if request.method == 'POST':  
        email = request.POST.get('email', '').strip()
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        confirmpassword = request.POST.get('confirm_password', '')

        # Validation
        errors = []
        
        if not username or not email or not password or not confirmpassword:
            errors.append('All fields are required.')
        
        if username and len(username) < 3:
            errors.append('Username must be at least 3 characters long.')
            
        if username and len(username) > 30:
            errors.append('Username must be less than 30 characters.')
            
        # Email validation
        if email:
            try:
                validate_email(email)
            except ValidationError:
                errors.append('Please enter a valid email address.')
        
        # Password validation (simplified)
        if password and len(password) < 8:
            errors.append('Password must be at least 8 characters long.')
            
        if password and not any(c.isupper() for c in password):
            errors.append('Password must contain at least one uppercase letter.')
            
        if password and not any(c.islower() for c in password):
            errors.append('Password must contain at least one lowercase letter.')
            
        if password and not any(c.isdigit() for c in password):
            errors.append('Password must contain at least one number.')
        
        if confirmpassword != password:
            errors.append("Passwords do not match.")
            
        if User.objects.filter(email=email).exists():
            errors.append("Email already exists.")
            
        if User.objects.filter(username=username).exists():
            errors.append("Username already exists.")
        
        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            try:
                user = User.objects.create_user(
                    username=username, 
                    email=email, 
                    password=password
                )
                messages.success(request, "Account created successfully!")
                return redirect('signin')
            except Exception as e:
                messages.error(request, "An error occurred while creating your account. Please try again.")

    return render(request, "signup.html")

def about(request):
    return render(request, 'about.html')

def signout(request):
    logout(request)
    request.session.flush()
    return redirect('home')

def contact(request):
    return render(request, 'contact.html')

def gallery(request):
    product = Product.objects.all()
    return render(request, 'gallery.html', {'product': product})

@login_required
def admin_page(request):
    # Get filter parameters
    category = request.GET.get('category', '')
    
    # Base queryset
    products = Product.objects.all()
    
    # Apply filters
    if category:
        products = products.filter(event__name=category)
    
    # Pagination
    paginator = Paginator(products, 9)  # Show 9 products per page
    page_number = request.GET.get('page', 1)
    products = paginator.get_page(page_number)
    
    context = {
        'products': products,
    }
    
    return render(request, 'admin_page.html', context)

@login_required
def admin_add(request):
    # Get all event types for the dropdown
    events = event.objects.all()
    
    if request.method == 'POST':
        # Extract form data
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        location = request.POST.get('location')
        event_id = request.POST.get('event')
        
        # Create new product
        product = Product(
            name=name,
            price=price,
            description=description,
            location=location,
            event_id=event_id
        )
        
        # Handle images
        if 'image' in request.FILES:
            product.image = request.FILES['image']
        if 'image1' in request.FILES:
            product.image1 = request.FILES['image1']
        if 'image2' in request.FILES:
            product.image2 = request.FILES['image2']
        if 'image3' in request.FILES:
            product.image3 = request.FILES['image3']
        if 'image4' in request.FILES:
            product.image4 = request.FILES['image4']
        
        # Save the product
        product.save()
        
        messages.success(request, f'Venue "{name}" has been added successfully!')
        return redirect('admin_page')
    
    context = {
        'events': events,
    }
    
    return render(request, 'admin_add.html', context)

@login_required
def admin_edit(request, product_id):
    # Get the product to edit
    product = get_object_or_404(Product, id=product_id)
    
    # Get all event types for the dropdown
    events = event.objects.all()
    
    if request.method == 'POST':
        # Extract form data
        product.name = request.POST.get('name')
        product.price = request.POST.get('price')
        product.description = request.POST.get('description')
        product.location = request.POST.get('location')
        product.event_id = request.POST.get('event')
        
        # Handle images
        if 'image' in request.FILES:
            product.image = request.FILES['image']
        if 'image1' in request.FILES:
            product.image1 = request.FILES['image1']
        if 'image2' in request.FILES:
            product.image2 = request.FILES['image2']
        if 'image3' in request.FILES:
            product.image3 = request.FILES['image3']
        if 'image4' in request.FILES:
            product.image4 = request.FILES['image4']
        
        # Save the product
        product.save()
        
        messages.success(request, f'Venue "{product.name}" has been updated successfully!')
        return redirect('admin_page')
    
    context = {
        'product': product,
        'events': events,
    }
    
    return render(request, 'admin_add.html', context)

@login_required()
def admin_remove(request, product_id):
    
    # Only process POST requests (for security)
    if request.method == 'POST':
        # Get the product to delete
        product = get_object_or_404(Product, id=product_id)
        product_name = product.name
        
        # Delete the product
        product.delete()
        
        messages.success(request, f'Venue "{product_name}" has been deleted successfully!')
    
    return redirect('admin_page')

def event_page(request, event_id):
    """
    Display detailed information about a specific product
    """
    product = get_object_or_404(Product, id=event_id)
    
    # Optionally get related products
    related_products = Product.objects.filter(event=product.event).exclude(id=event_id)[:3]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    
    return render(request, 'event_page.html', context)


def order_payment(request):
    if request.method == "POST":
        name = request.POST.get("name")
        amount = request.POST.get("amount")

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        razorpay_order = client.order.create(
            {"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"}
        )

        order_id = razorpay_order['id']
        order = Order.objects.create(
            name=name, amount=amount, provider_order_id=order_id
        )
        order.save()

        return render(
            request,
            "index.html",
            {
                "callback_url": "http://" + "127.0.0.1:8000" + "razorpay/callback",
                "razorpay_key": settings.RAZORPAY_KEY_ID,
                "order": order,

            },
        )

    return render(request, "index.html")


@csrf_exempt
def callback(request):

    def verify_signature(response_data):
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        return client.utility.verify_payment_signature(response_data)

    if "razorpay_signature" in request.POST:
        payment_id = request.POST.get("razorpay_payment_id", "")
        provider_order_id = request.POST.get("razorpay_order_id", "")
        signature_id = request.POST.get("razorpay_signature", "")

        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.signature_id = signature_id
        order.save()

        if not verify_signature(request.POST):
            order.status = PaymentStatus.SUCCESS
            order.save()
            return render(request, "callback.html", context={"status": order.status}) 
            # or return redirect(function name of callback giving html page)
        else:
            order.status = PaymentStatus.FAILURE
            order.save()
            return render(request, "callback.html", context={"status": order.status}) 
            # or return redirect(function name of callback giving html page)
    else:
     payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
     provider_order_id = json.loads(request.POST.get("error[metadata]")).get("order_id")

     order = Order.objects.get(provider_order_id=provider_order_id)
     order.payment_id = payment_id
     order.status = PaymentStatus.FAILURE
     order.save()

    return render(request, "callback.html", context={"status": order.status}) 
    # or return redirect(function name of callback giving html page)

def index(request,product_id):
    # Get all events to display on home page
    product_id = event.objects.all()
    return render(request, 'index.html', {'product_id': product_id})

@login_required
def checkout(request, product_id):
    """
    View for checking out and booking a venue
    """
    product = get_object_or_404(Product, id=product_id)
    food_items = food.objects.all()
    user_addresses = Address.objects.filter(user=request.user)
    
    if request.method == 'POST':
        # Extract form data
        name = request.POST.get('name')
        date = request.POST.get('date')
        duration = request.POST.get('duration')
        total_price = Decimal(request.POST.get('total_price', 0))
        
        # Handle address (existing or new)
        address_id = request.POST.get('address_id')
        if address_id:
            address = get_object_or_404(Address, id=address_id, user=request.user)
        else:
            # Create new address
            contact_name = request.POST.get('contact_name')
            contact_address = request.POST.get('contact_address')
            contact_phone = request.POST.get('contact_phone')
            
            if contact_name and contact_address and contact_phone:
                address = Address(
                    user=request.user,
                    name=contact_name,
                    address=contact_address,
                    phone=contact_phone
                )
                address.save()
            else:
                address = None
        
        # Create booking
        booking = Booking(
            user=request.user,
            product=product,
            name=name,
            date=date,
            duration=duration,
            address=address,
            total_price=total_price,
            status='pending'
        )
        booking.save()
        
        # Handle food items - FIXED: Store price when creating BookingFood
        food_items_selected = request.POST.getlist('food_items')
        for food_id in food_items_selected:
            food_item = get_object_or_404(food, id=food_id)
            quantity = int(request.POST.get(f'food_quantity_{food_id}', 1))
            
            BookingFood.objects.create(
                booking=booking,
                food=food_item,
                quantity=quantity,
                price=Decimal(str(food_item.price))  # Store the price at booking time
            )
        
        messages.success(request, "Your booking has been placed successfully!")
        return redirect('booking_confirmation', booking_id=booking.id)
    
    context = {
        'product': product,
        'food_items': food_items,
        'addresses': user_addresses
    }
    return render(request, 'checkout.html', context)


@login_required
def booking_confirmation(request, booking_id):
    """
    View for displaying booking confirmation - QUICK FIX VERSION
    """
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    booking_food_items = BookingFood.objects.filter(booking=booking)
    
    # Calculate venue total
    venue_total = 0
    if booking.duration and booking.product and booking.product.price:
        duration = 12 if booking.duration == 'full' else int(booking.duration)
        venue_total = float(booking.product.price) * duration
    
    # Calculate food total - QUICK FIX: Calculate directly without method
    food_total = 0
    food_items_with_totals = []
    
    for item in booking_food_items:
        # Calculate total directly (works with current model)
        if item.price:
            item_total = float(item.price) * item.quantity
        else:
            item_total = float(item.food.price) * item.quantity
        
        food_total += item_total
        
        # Create a dict with the item data and calculated total
        food_items_with_totals.append({
            'food_item': item.food,
            'quantity': item.quantity,
            'price': item.price or item.food.price,
            'total_price': item_total,
            'booking_food_obj': item
        })
    
    # Add calculated totals to booking object for template access
    booking.venue_total = venue_total
    booking.food_total = food_total
    
    context = {
        'booking': booking,
        'food_items': food_items_with_totals
    }
    return render(request, 'booking_confirmation.html', context)

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    paginator = Paginator(bookings, 10)  # 10 bookings per page
    page = request.GET.get('page')
    bookings = paginator.get_page(page)
    
    return render(request, 'my_bookings.html', {'bookings': bookings})

def cancel_booking(request, booking_id):
    """
    Cancel a booking (AJAX endpoint)
    """
    try:
        booking = get_object_or_404(Booking, id=booking_id, user=request.user)
        
        # Only allow cancellation of pending bookings
        if booking.status != 'pending':
            return JsonResponse({
                'success': False, 
                'message': 'Only pending bookings can be cancelled'
            })
        
        # Update booking status
        booking.status = 'cancelled'
        booking.save()
        
        messages.success(request, f'Booking #{booking.id} has been cancelled successfully.')
        
        return JsonResponse({
            'success': True, 
            'message': 'Booking cancelled successfully'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False, 
            'message': 'Error cancelling booking'
        })
    
# food section #

def food_list(request):
    """
    Display all food items in the database
    """
    foods = food.objects.all()
    context = {
        'foods': foods
    }
    return render(request, 'food_list.html', context)

# food section #
@login_required
def add_food(request):
    """
    View for adding a new food item
    """
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        quantity = request.POST.get('quantity')
        
        # Create new food item
        new_food = food(
            name=name,
            price=price,
            description=description,
            quantity=quantity if quantity else None
        )
        new_food.save()
        
        messages.success(request, "Food item added successfully!")
        return redirect('food_list')
    
    return render(request, 'add_food.html')

def edit_food(request, food_id):
    """
    View for editing an existing food item
    """
    food_item = get_object_or_404(food, id=food_id)
    
    if request.method == 'POST':
        food_item.name = request.POST.get('name')
        food_item.price = request.POST.get('price')
        food_item.description = request.POST.get('description')
        quantity = request.POST.get('quantity')
        food_item.quantity = quantity if quantity else None
        
        food_item.save()
        
        messages.success(request, "Food item updated successfully!")
        return redirect('food_list')
    
    context = {
        'food_item': food_item
    }
    return render(request, 'add_food.html', context)

def delete_food(request, food_id):
    """
    View for deleting a food item
    """
    food_item = get_object_or_404(food, id=food_id)
    food_item.delete()
    
    messages.success(request, "Food item deleted successfully!")
    return redirect('food_list')

def search(request):    
    query = request.GET.get('q', '')  # Get search query from GET request
    # Filter products by name (case insensitive)
    products = Product.objects.filter(name__icontains=query)

    return render(request, 'user/search_result.html', {
        'products': products,
        'query': query,
    })