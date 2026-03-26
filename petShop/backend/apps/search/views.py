from django.http import HttpRequest
from django.shortcuts import render
from apps.catalog.models import Product
from django.contrib import messages
from django.db.models import Q

# Create your views here.
def search(request: HttpRequest):
    if request.method == 'POST':
        searchbox = request.POST.get('searchbox')
        products = Product.objects.filter(Q(name__icontains=searchbox) | Q(description__icontains=searchbox) | Q(category__name__icontains=searchbox) | Q(tags__icontains=searchbox))
        if products.count() == 0:
            messages.error(request, 'Ничего не найдено')
        return render(request, 'catalog.html', {'products': products})
    else:
        return render(request, 'catalog.html')