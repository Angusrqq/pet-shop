from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
# Create your models here.

class Category(MPTTModel):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="category_images/")
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    
    class MPTTMeta:
        order_insertion_by = ['name']
        
    class Meta:
        verbose_name_plural = 'Categories'
        
    def __str__(self):
        return self.name
    
    def get_products(self):
        from apps.catalog.models import Product
        categories = self.get_descendants(include_self=True)
        return Product.objects.filter(category__in=categories)