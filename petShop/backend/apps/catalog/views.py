from django.shortcuts import render
from django.http import HttpRequest
from apps.catalog.models import Product
from apps.categories.models import Category

# Create your views here.

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