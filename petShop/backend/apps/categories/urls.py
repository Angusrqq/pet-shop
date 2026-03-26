from django.urls import path
from . import views

app_name = 'categories'

urlpatterns = [
    path('', views.categories, name='category_list'),
    path('<int:pk>/', views.categories, name='category_detail'),
]
