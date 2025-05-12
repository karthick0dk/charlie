# shop/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm
from django.contrib.auth.models import User
from .models import Profile
from django.contrib import messages

def register_view(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            role = form.cleaned_data['role']
            user = User.objects.create_user(username=username, password=password)
            user.save()
            user.profile.role = role  # Link role to Profile
            user.profile.save()
            messages.success(request, "Registered Successfully. Please login.")
            return redirect('login')
    return render(request, 'shop/register.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid credentials.")
    return render(request, 'shop/login.html')


from django.contrib.auth.decorators import login_required

@login_required
def dashboard_view(request):
    role = request.user.profile.role
    return render(request, 'shop/dashboard.html', {'role': role})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product
from .forms import ProductForm

# Helper to get role
def get_user_role(user):
    return user.profile.role if hasattr(user, 'profile') else None

@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products, 'role': get_user_role(request.user)})

@login_required
def product_create(request):
    role = get_user_role(request.user)
    if role not in ['manager', 'assistant']:
        return redirect('product_list')
    form = ProductForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('product_list')
    return render(request, 'shop/product_form.html', {'form': form, 'role': role})

@login_required
def product_update(request, pk):
    role = get_user_role(request.user)
    if role not in ['manager', 'assistant']:
        return redirect('product_list')
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid():
        form.save()
        return redirect('product_list')
    return render(request, 'shop/product_form.html', {'form': form, 'role': role})

@login_required
def product_delete(request, pk):
    role = get_user_role(request.user)
    if role != 'manager':
        return redirect('product_list')
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        return redirect('product_list')
    return render(request, 'shop/product_confirm_delete.html', {'product': product})
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    role = request.user.profile.role  # getting role from profile
    return render(request, 'shop/dashboard.html', {'role': role})
from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('login')

