from django.urls import path
from . import views

app_name = 'catalog'


urlpatterns = [
    path('', views.catalog, name='catalog'),
    path('<int:category_pk>', views.catalog, name='catalog'),
    path('product/<int:pk>', views.product, name='product'),
]