from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .cart import Cart
from core.models import Product
import json

def cart(request):
    cart = Cart(request)
    return render(request, 'cart.html', {'cart': cart})

@require_POST
def add_to_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product, quantity=1)
    return redirect('cart:cart')

@require_POST
def remove_from_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart')

@require_POST
def cart_decrement(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    item = cart.cart.get(str(product_id))
    if item:
        if item['quantity'] > 1:
            cart.add(product, quantity=-1)
        else:
            cart.remove(product)
    return redirect('cart:cart')

# @require_POST
# def cart_update(request, product_id):
#     cart = Cart(request)
#     product = get_object_or_404(Product, id=product_id)
#     data = json.loads(request.body)
#     quantity = int(data.get('quantity', 1))
#     cart.add(product, quantity=quantity, override_quantity=True)
#     return redirect('cart:cart')