
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User



def home(request):
    return render(request,'home.html')
    
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
            if  user.is_superuser:
                return redirect('admin')
            else:
                return redirect('home')
        else:
            messages.error(request, "Invalid credentials.")
    
    return render(request, 'signin.html')

def signup(request):
    if request.method == 'POST':  
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')

        if not username or not email or not password or not confirmpassword:
            messages.error(request, 'All fields are required.')
        elif confirmpassword != password:
            messages.error(request, "Passwords do not match.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
        else:
            # Corrected line to use create_user
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, "Account created successfully!")
            return redirect('signin')  

    return render(request, "signup.html")

def about(request):
    return render(request, 'about.html')

def signout(request):
    logout(request)
    request.session.flush()
    return redirect('home')

def weding(request):
    return render(request, 'weding.html')

def contact(request):
    return render(request, 'contact.html')

def gallery(request):
    return render(request, 'gallery.html')

def wed_details(request):
    return render(request, 'wed_details.html')