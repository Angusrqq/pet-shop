from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpRequest
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomAuthForm

def main(request):
    return render(request, 'main.html')

def about(request):
    return render(request, 'about.html')

def catalog(request):
    return render(request, 'catalog.html')

def delivery(request):
    return render(request, 'delivery.html')

def auth(request):
    return render(request, 'auth.html')

def cart(request):
    return render(request, 'cart.html')

def register(request):
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('auth')
    context = {'form': form}
    return render(request, 'register.html', context)

def auth(request: HttpRequest):
    form = CustomAuthForm()
    if request.method == 'POST':
        form = CustomAuthForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('main')
    context = {'form': form}
    return render(request, 'auth.html', context)

@login_required
def set_theme(request: HttpRequest):
    if request.method == 'POST':
        theme = request.POST.get('theme', 'light')
        if theme in ('light', 'dark'):
            request.user.theme = theme
            request.user.save(update_fields=['theme'])
            return JsonResponse({'status': 'ok', 'theme': theme})
    return JsonResponse({'status': 'error'}, status=400)