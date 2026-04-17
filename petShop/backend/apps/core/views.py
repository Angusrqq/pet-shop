from django.shortcuts import render
from apps.catalog.models import Product
from django.db.models import Count, Sum

def main(request):
    latest_products = Product.objects.order_by('-date_added')[:5]
    discounted_products = Product.objects.filter(discount__isnull=False).distinct()
    top_products = Product.objects.annotate(total_quantity=Sum('purchase__quantity')).order_by('-total_quantity')[:10]
    
    context = {
        'products': latest_products,
        'products_count': latest_products.count(),
        'discounted_products': discounted_products,
        'top_products': top_products,
    }
    return render(request, 'main.html', context)

def about(request):
    return render(request, 'about.html')

def delivery(request):
    return render(request, 'delivery.html')