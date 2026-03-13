from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('about/', views.about, name='about'),
    path('catalog/', views.catalog, name='catalog'),
    path('product/<int:pk>', views.product, name='product'),
    path('delivery/', views.delivery, name='delivery'),
    path('auth/', views.auth, name='auth'),
    path('cart/', views.cart, name='cart'),
    path('set_theme/', views.set_theme, name='set_theme'),
    path('login/', views.auth, name='login'),
    path('register/', views.register, name='register'),
]