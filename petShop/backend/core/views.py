from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse, HttpRequest
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomAuthForm
from .models import Product, Category
from django.db.models import Q

def main(request):
    return render(request, 'main.html')

def about(request):
    return render(request, 'about.html')

def catalog(request: HttpRequest, category_pk = None):
    if category_pk:
        if not Category.objects.filter(pk=category_pk).exists():
            products = Product.objects.all()
        else:
            products = Category.objects.get(pk=category_pk).get_products()
    else:
        products = Product.objects.all()
    return render(request, 'catalog.html', {'products': products})

def product(request, pk):
    product = Product.objects.get(pk=pk)
    return render(request, 'product.html', {'product': product})

def delivery(request):
    return render(request, 'delivery.html')


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

@login_required(login_url='core:auth')
def logout_page(request):
    logout(request)
    messages.info(request, 'Вы вышли из аккаунта')
    return redirect('core:auth')

def register(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect('core:main')
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегистрировались!')
            return redirect('core:auth')
        else:
            messages.error(request, form.errors)
    context = {'form': form}
    return render(request, 'register.html', context)

def categories(request, pk = None):
    if pk:
        parent = get_object_or_404(Category, pk=pk)
        categories = parent.get_children()
    else:
        parent = None
        categories = Category.objects.root_nodes()
    return render(request, 'categories.html', {"categories": categories, "parent": parent})

def search(request: HttpRequest):
    if request.method == 'POST':
        searchbox = request.POST.get('searchbox')
        products = Product.objects.filter(Q(name__icontains=searchbox) | Q(description__icontains=searchbox) | Q(category__name__icontains=searchbox) | Q(tags__icontains=searchbox))
        if products.count() == 0:
            messages.error(request, 'Ничего не найдено')
        return render(request, 'catalog.html', {'products': products})
    else:
        return render(request, 'catalog.html')