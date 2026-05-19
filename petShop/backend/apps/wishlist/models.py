from django.db import models
from django.conf import settings
from apps.catalog.models import Product

class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, related_name='wishlist_items')
    session_key = models.CharField(max_length=40, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlist_users')
    creation_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'product'] if not settings.DATABASES['default']['ENGINE'].startswith('django.db.backends.sqlite3') else []
        ordering = ['-creation_date']