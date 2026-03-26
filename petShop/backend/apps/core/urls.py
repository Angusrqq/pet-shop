from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.main, name='main'),
    path('about/', views.about, name='about'),
    path('delivery/', views.delivery, name='delivery'),
]