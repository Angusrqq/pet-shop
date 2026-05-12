from django.http import HttpRequest
from django.shortcuts import render
from apps.catalog.models import Product
from django.contrib import messages
from django.db.models import Q
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

# Create your views here.
def deprecated_search(request: HttpRequest):
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
    
def search(request: HttpRequest):
     if request.method == 'POST':
          user_query = request.POST.get('searchbox')
          search_vector = SearchVector('name', 'description', 'category__name', 'tags')
          search_query = SearchQuery(user_query, search_type='websearch')
          products = Product.objects.annotate(
               rank=SearchRank(search_vector, search_query, weights = [1, 0.5, 0.3, 0.3])
          ).filter(rank__gte=0.3).order_by("rank")
          if products.count() == 0:
               messages.error(request, 'Ничего не найдено')
          return render(request, 'catalog.html', {'products': products})
     else:
          return render(request, 'catalog.html')
