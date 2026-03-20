from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .cart import Cart
from core.models import Product
from django.contrib import messages
import json

def cart(request):
    cart = Cart(request)
    return render(request, 'cart.html', {'cart': cart})

@require_POST
def add_to_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    if cart.cart.get(str(product_id)) and product.stock < cart.cart[str(product_id)]['quantity'] + 1:
        messages.info(request, 'Недостаточно товара в наличии')
        return redirect('cart:cart')

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

@require_POST
def clear_cart(request):
    cart = Cart(request)
    cart.clear_cart()
    return redirect('cart:cart')

@require_POST
def cart_update(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    if quantity > product.stock:
        quantity = product.stock
    if quantity < 1:
        cart.remove(product)
    else:
        cart.add(product, quantity=quantity, override_quantity=True)
    return redirect('cart:cart')