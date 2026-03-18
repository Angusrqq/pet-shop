from decimal import Decimal

from django.conf import settings
from django.http import JsonResponse, HttpRequest
from ..models import Product

class Cart:
    def __init__(self, request: HttpRequest):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        
    def add(self, product: Product, quantity=1, override_quantity=False):
        product_id = str(product.pk)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                    'price': str(product.price)}
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()
        
    def remove(self, product:Product):
        product_id = str(product.pk)
        if product_id in self.cart:
            del self.cart[product_id]
        self.save()
        
    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.pk)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = Decimal(item['price']) * item['quantity']
            yield item
            
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    
    def get_total_cart_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item
                    in self.cart.values())
        
    def clear_cart(self):
        for key in list(self.cart.keys()):
            del self.cart[key]
        self.save()