from django.shortcuts import render
from .cart import Cart
from core.models import Product

def cart(request):
    return render(request, 'cart.html')

def add_to_cart():
    pass

def remove_from_cart():
    pass

def cart_update():
    pass