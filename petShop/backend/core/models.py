from django.db import models
from django.conf import settings

def generate_track():
    from random import randint
    unique_number = randint(1000000000, 9999999999)
    while Orders.objects.filter(track_number=unique_number).exists():
        unique_number = randint(1000000000, 9999999999)
    return str(unique_number)
# Create your models here.

class Orders(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=100)
    client_last_name = models.CharField(blank=True, max_length=100)
    client_email = models.EmailField()
    client_phone = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    creation_date = models.DateField(auto_now_add=True)
    address = models.TextField(blank=True)
    track_number = models.CharField(blank=True, unique=True, null=True, default=generate_track)

class Products(models.Model):
    tags = models.CharField()
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to="product_images/")
    stock = models.IntegerField(default=0)
    price = models.FloatField()

class Purchases(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    price = models.FloatField()
    quantity = models.IntegerField()

    def total_price(self):
        return self.price * self.quantity