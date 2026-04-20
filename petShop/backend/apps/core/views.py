from django.shortcuts import render
from apps.catalog.models import Product, Discount
from django.db.models import Count, Sum

def main(request):
    latest_products = Product.objects.order_by('-date_added')[:5]
    discounted_products = Discount.get_all_discounted_products()
    discounted_products = set(discounted_products)
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

def error_400(request, exception=None):
    return render(request, 'error.html', {'code': 400, 'message': 'Неверный запрос'}, status=400)

def error_403(request, exception=None):
    return render(request, 'error.html', {'code': 403, 'message': 'Нет доступа'}, status=403)

def error_404(request, exception=None):
    return render(request, 'error.html', {'code': 404, 'message': 'Страница не найдена'}, status=404)

def error_500(request):
    return render(request, 'error.html', {'code': 500, 'message': 'Ошибка сервера'}, status=500)