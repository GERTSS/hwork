from . import views
from rest_framework.routers import DefaultRouter

from django.urls import path, include

router = DefaultRouter()
router.register('products/', views.ProductViewSet)
router.register('orders/', views.OrderViewSet)

app_name = 'shopapp'

urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.list_urls, name='index'),
    path('products/', views.ProductsListView.as_view(), name='list_products'),
    path('products/<int:pk>', views.ProductDetailsView.as_view(), name='product_details'),
    path('orders/', views.OrdersListView.as_view(), name='list_orders'),
    path('orders/<int:pk>', views.OrdersDetailsView.as_view(), name='order_details'),
    path('upload/', views.upload_file, name='upload_file'),
    path('products/create/', views.ProductCreateView.as_view(), name='create_products'),
    path('orders/create/', views.OrderCreateView.as_view(), name='create_order'),
    path('products/update/<int:pk>', views.ProductUpdateView.as_view(), name='update_products'),
    path('orders/update/<int:pk>', views.OrderUpdateView.as_view(), name='update_order'),
    path('products/archive/<int:pk>', views.ProductArchiveView.as_view(), name='archive_product'),
    path('orders/archive/<int:pk>', views.OrderArchiveView.as_view(), name='archive_order'),
    path('orders/export', views.OrderExportView.as_view(), name='orders_get_copy'),
]
