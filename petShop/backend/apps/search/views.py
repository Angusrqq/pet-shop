from django.http import HttpRequest
from django.shortcuts import render
from apps.catalog.models import Product
from django.contrib import messages
from django.db.models import Q

# Create your views here.
def search(request: HttpRequest):
    if request.method == 'POST':
        keywords = request.POST.get('searchbox').split()
        queryset = Product.objects.all()
        for word in keywords:
                queryset = queryset.filter(Q(name__icontains=word) | Q(description__icontains=word) | Q(category__name__icontains=word) | Q(tags__icontains=word))
        products = queryset
        if products.count() == 0:
            messages.error(request, 'Ничего не найдено')
        return render(request, 'catalog.html', {'products': products})
    else:
        return render(request, 'catalog.html')