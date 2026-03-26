from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.contrib import messages
from .forms import CustomAuthForm, CustomUserCreationForm
# Create your views here.

def auth(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect('core:main')
    form = CustomAuthForm()
    if request.method == 'POST':
        form = CustomAuthForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password) # doesnt the form.is_valid() check it already?

            if user is not None:
                login(request, user)
                messages.success(request, 'Вы успешно авторизовались!')
                return redirect('core:main')
        else:
            # messages.error(request, form.errors)
            messages.error(request, 'Неправильный логин или пароль')

    context = {'form': form}
    return render(request, 'auth.html', context)

@login_required(login_url='users:auth')
def logout_page(request):
    logout(request)
    messages.info(request, 'Вы вышли из аккаунта')
    return redirect('users:auth')

def register(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect('core:main')
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегистрировались!')
            return redirect('users:auth')
        else:
            messages.error(request, form.errors)
    context = {'form': form}
    return render(request, 'register.html', context)