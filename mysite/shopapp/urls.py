from . import views

from django.urls import path

urlpatterns = [
    path('', views.list_urls, name='index'),
    path('products/', views.list_products, name='list_products'),
    path('orders/', views.list_orders, name='list_orders'),
]
