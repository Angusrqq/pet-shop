from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('auth/', views.auth, name='auth'),
    path('logout/', views.logout_page, name='logout'),
    path('register/', views.register, name='register'),
]
