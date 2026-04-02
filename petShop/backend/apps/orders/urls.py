from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    # path('orders/', views.orders, name='orders'),
    path('checkout/', views.checkout, name='checkout'),
    path('success/', views.success, name='success'),
]