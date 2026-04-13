from django.shortcuts import render
from apps.catalog.models import Product

def main(request):
    products = Product.objects.all()
    return render(request, 'main.html', {'products': products})

def about(request):
    return render(request, 'about.html')

def delivery(request):
    return render(request, 'delivery.html')