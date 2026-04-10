from django.shortcuts import get_object_or_404, render
from django.http import HttpRequest
from apps.catalog.models import Product
from apps.categories.models import Category

# Create your views here.

def catalog(request: HttpRequest, category_pk = None):
    categories = Category.objects.root_nodes()
    parent = None
    if category_pk:
        parent = get_object_or_404(Category, pk=category_pk)
        categories = parent.get_children()
        products = parent.get_products()
    else:
        products = Product.objects.all()
    return render(request, 'catalog.html', {'products': products, 'categories': categories, 'parent': parent})

def product(request, pk):
    product = Product.objects.get(pk=pk)
    return render(request, 'product.html', {'product': product})