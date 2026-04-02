from django.shortcuts import redirect, render
from django.urls import reverse
from apps.cart.cart import Cart
from apps.orders.forms import OrderCreationForm
from apps.orders.models import Order, Purchase

def checkout(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreationForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.payment_method = request.POST.get('payment-method')
            order.delivery_method = request.POST.get('delivery-method')
            order.save()
            for item in cart:
                Purchase.objects.create(
                    order = order,
                    product = item['product'],
                    price = item['price'],
                    quantity = item['quantity']
                )
            cart.clear_cart()
            request.session['order_id'] = order.id
            return redirect(reverse('orders:success'))
    else:
        form = OrderCreationForm()
    return render(request, 'checkout.html', {'cart': cart, 'form': form})
    
def success(request):
    order_id = request.session.get('order_id')
    order = Order.objects.get(id = order_id) if order_id else None
    return render(request, 'success.html', {'order': order})