from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_POST
from .cart import Cart
from apps.catalog.models import Product
from django.contrib import messages

def cart(request):
    cart = Cart(request)
    return render(request, 'cart.html', {'cart': cart})

@require_POST
def add_to_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    next_url = request.POST.get('next') or request.GET.get('next') or '/'

    if cart.cart.get(str(product_id)) and product.stock < cart.cart[str(product_id)]['quantity'] + 1:
        messages.error(request, 'Недостаточно товара в наличии')
        return redirect(next_url)
    
    if cart.cart.get(str(product_id)) == None:
        messages.success(request, 'Товар добавлен в корзину!')

    cart.add(product, quantity=1)
    return redirect(next_url)

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
    messages.success(request, 'Корзина очищена!')
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