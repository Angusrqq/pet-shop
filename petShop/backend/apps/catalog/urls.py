from django.urls import path
from . import views

app_name = 'catalog'


urlpatterns = [
    path('catalog/', views.catalog, name='catalog'),
    path('catalog/<int:category_pk>', views.catalog, name='catalog'),
    path('product/<int:pk>', views.product, name='product'),
]