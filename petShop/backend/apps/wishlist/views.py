from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from apps.catalog.models import Product
from .models import Wishlist

def get_wishlist(request):
    if request.user.is_authenticated:
        return Wishlist.objects.filter(user=request.user)
    return Wishlist.objects.filter(session_key=request.session.session_key)

def wishlist(request):
    items = get_wishlist(request).select_related('product')
    return render(request, 'wishlist.html', {'items': items})

@require_POST
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
        if not created:
            item.delete()
            in_wishlist = False
        else:
            in_wishlist = True
    else:
        if not request.session.session_key:
            request.session.create()
        item = Wishlist.objects.filter(session_key=request.session.session_key, product=product)
        if item.exists():
            item.delete()
            in_wishlist = False
        else:
            Wishlist.objects.create(session_key=request.session.session_key, product=product)
            in_wishlist = True

    return JsonResponse({
        'in_wishlist': in_wishlist,
        'count': get_wishlist(request).count()
    })
