from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_POST

def wishlist(request):
    return render(request, 'wishlist.html')

# @require_POST
# def add_to_wishlist(request, product_id):
#     cart = Cart(request)
#     product = get_object_or_404(Product, id=product_id)
#     next_url = request.POST.get('next') or request.GET.get('next') or 'cart:cart'

#     if cart.cart.get(str(product_id)) and product.stock < cart.cart[str(product_id)]['quantity'] + 1:
#         messages.error(request, 'Недостаточно товара в наличии')
#         return redirect(next_url)
    
#     if cart.cart.get(str(product_id)) == None:
#         messages.success(request, 'Товар добавлен в корзину!')

#     cart.add(product, quantity=1)
    
#     if(next_url == 'cart:cart'):
#         return redirect('cart:cart')
    
#     return JsonResponse({
#         'cart_count': len(cart),
#         'messages': get_messages_list(request)
#     })
