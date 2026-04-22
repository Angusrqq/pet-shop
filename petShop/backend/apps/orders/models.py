from django.db import models
from django.conf import settings
from apps.catalog.models import Product
# Create your models here.

DELIVERY_COST = 500

def generate_track():
    from uuid import uuid4
    while True:
        unique_id = uuid4().int % 1_000_000_000
        unique_id = f"{unique_id:09d}"
        if not Order.objects.filter(track_number=unique_id).exists():
            return unique_id

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

    def get_total_price(self):
        total = 0
        items = Purchase.objects.filter(order=self)
        for item in items:
            total += item.total_price()
        if self.delivery_method == 'delivery':
            total += DELIVERY_COST
        return total


class Purchase(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    quantity = models.IntegerField()

    def total_price(self):
        return self.price * self.quantity