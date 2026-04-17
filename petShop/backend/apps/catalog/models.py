from django.db import models
from apps.categories.models import Category
# Create your models here.

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    tags = models.TextField()
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to="product_images/")
    stock = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    date_added = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    
    def get_tags_list(self):
        return self.tags.split(",")
    
    def has_discount(self):
        # check product-specific discount
        if Discount.objects.filter(product=self, is_active=True).exists():
            return True
        # check category and all its ancestors
        category_ids = self.category.get_ancestors(include_self=True).values_list('id', flat=True)
        return Discount.objects.filter(category__in=category_ids, is_active=True).exists()
    
    def get_discount(self):
        category_ids = self.category.get_ancestors(include_self=True).values_list('id', flat=True)
        return Discount.objects.filter(
            models.Q(product=self) | models.Q(category__in=category_ids),
            is_active=True
        ).order_by('-percent').first()

    def discounted_price(self):
        discount = self.get_discount()
        if discount:
            return self.price - (self.price * discount.percent / 100)
        return self.price
    
    def get_top_discount_percent(self):
        category_ids = self.category.get_ancestors(include_self=True).values_list('id', flat=True)
        return Discount.objects.filter(
            models.Q(product=self) | models.Q(category__in=category_ids),
            is_active=True
        ).order_by('-percent').first().percent

class Discount(models.Model):
    name = models.CharField(max_length=100, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    percent = models.IntegerField()
    is_active = models.BooleanField(default=False)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True, blank=True, null=True)
