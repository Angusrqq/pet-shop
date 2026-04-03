from django.db import models
from django.conf import settings
from apps.catalog.models import Product
# Create your models here.

DELIVERY_COST = 500

def generate_track():
    from random import randint
    unique_number = randint(1000000000, 9999999999)
    # stupid implementation, whatever
    while Order.objects.filter(track_number=unique_number).exists():
        unique_number = randint(1000000000, 9999999999)
    return str(unique_number)
# Create your models here.

class Order(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    session_key = models.CharField(max_length=40, blank=True, null=True)
    client_name = models.CharField(max_length=100)
    client_last_name = models.CharField(blank=True, max_length=100)
    client_email = models.EmailField()
    client_phone = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    creation_date = models.DateTimeField(auto_now_add=True)
    delivery_method = models.CharField(max_length=100)
    address = models.TextField(blank=True)
    track_number = models.CharField(blank=True, unique=True, null=True, default=generate_track)

class Purchase(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    quantity = models.IntegerField()

    def total_price(self):
        return self.price * self.quantity