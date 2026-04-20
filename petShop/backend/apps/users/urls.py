from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('auth/', views.auth, name='auth'),
    path('logout/', views.logout_page, name='logout'),
    path('register/', views.register, name='register'),
    path('account/', views.account, name='account'),
    path('orders/', views.orders, name='orders'),
    path('orders/<int:order_id>/', views.order, name='order'),
    path('change-password/', views.change_password, name='change_password'),
]
