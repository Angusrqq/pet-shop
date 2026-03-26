from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.main, name='main'),
    path('about/', views.about, name='about'),
    path('catalog/', views.catalog, name='catalog'),
    path('product/<int:pk>', views.product, name='product'),
    path('delivery/', views.delivery, name='delivery'),
    path('auth/', views.auth, name='auth'),
    path('login/', views.auth, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('register/', views.register, name='register'),
    path('categories/', views.categories, name='categories'),
    path('search', views.search, name='search'),
]