from . import views
from .sitemaps import ShopSitemap

from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from django.urls import path, include
from django.contrib.sitemaps.views import sitemap

router = DefaultRouter()
router.register('products/', views.ProductViewSet)
router.register('orders/', views.OrderViewSet)

app_name = 'shopapp'

sitemaps={
    'shop': ShopSitemap
}

urlpatterns = [
    path('products/latest/feed/', views.LatestProductsFeed(), name='feed'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('api/', include(router.urls)),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/doc/', SpectacularSwaggerView.as_view(url_name='shopapp:schema'), name='swagger'),
    path('', views.list_urls, name='index'),
    path('users/<int:user_id>/orders/export/', views.UserOrdersAPIView.as_view(), name='user_orders_export'),
    path('users/<int:user_id>/orders/', views.UserOrdersListView.as_view(), name='user_orders'),
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
