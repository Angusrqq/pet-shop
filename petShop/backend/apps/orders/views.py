from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse
from apps.cart.cart import Cart
from apps.orders.forms import OrderCreationForm
from apps.orders.models import Order, Purchase, DELIVERY_COST
from django.contrib import messages

def checkout(request: HttpRequest):
    cart = Cart(request)
    form = OrderCreationForm()
    if(request.user.is_authenticated):
        form.fields['client_name'].initial = request.user.first_name
        form.fields['client_last_name'].initial = request.user.last_name
        form.fields['client_email'].initial = request.user.email
    if request.method == 'POST':
        form = OrderCreationForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user_id = request.user
            else:
                order.session_key = request.session.session_key
            order.save()
            for item in cart:
                Purchase.objects.create(
                    order = order,
                    product = item['product'],
                    price = item['price'],
                    quantity = item['quantity']
                )
                product = item['product']
                product.stock -= item['quantity']
                product.save()
            cart.clear_cart()
            request.session['order_id'] = order.id
            return redirect(reverse('orders:success'))
        else:
            messages.error(request, form.errors)
    return render(request, 'checkout.html', {'cart': cart, 'form': form, 'delivery_cost': DELIVERY_COST})
    
def success(request):
    order_id = request.session.get('order_id')
    order = Order.objects.get(id = order_id) if order_id else None
    return render(request, 'success.html', {'order': order})