from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpRequest
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomAuthForm
from .models import Product

def main(request):
    return render(request, 'main.html')

def about(request):
    return render(request, 'about.html')

def catalog(request):
    products = Product.objects.all()
    return render(request, 'catalog.html', {'products': products})

def product(request, pk):
    product = Product.objects.get(pk=pk)
    return render(request, 'product.html', {'product': product})

def delivery(request):
    return render(request, 'delivery.html')

def auth(request: HttpRequest):
    form = CustomAuthForm()
    if request.method == 'POST':
        form = CustomAuthForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password) # doesnt the form.is_valid() check it already?

            if user is not None:
                login(request, user)
                return redirect('main')
            else:
                messages.info(request, 'Неправильный логин или пароль')

    context = {'form': form}
    return render(request, 'auth.html', context)

def logout_page(request):
    logout(request)
    return redirect('auth')

def register(request: HttpRequest):
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегистрировались!')
            return redirect('auth')
    context = {'form': form}
    return render(request, 'register.html', context)