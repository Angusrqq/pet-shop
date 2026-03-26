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
    
    def get_tags_list(self):
        return self.tags.split(",")