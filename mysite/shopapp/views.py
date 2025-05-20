from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponseRedirect, HttpResponseForbidden, JsonResponse
from django.urls import get_resolver, Resolver404, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

import mysite.settings
from shopapp.models import Product, Order
from shopapp.mixins import CanUpdateProductMixin
import os
import uuid
import logging
from shopapp.forms import ProductForm, OrderForm

logger = logging.getLogger('shoapapp')


def list_urls(request: HttpRequest):
    urls = []
    urlconf = get_resolver()
    all_urls = urlconf.url_patterns

    def recursive_handler(patterns, prefix='/'):
        for pattern in patterns:
            try:
                if hasattr(pattern, 'url_patterns'):
                    recursive_handler(pattern.url_patterns, prefix + str(pattern.pattern))
                else:
                    test_url = prefix + str(pattern.pattern)
                    if test_url == '/shop/products/create/':
                        if not request.user.has_perm('shopapp.add_product'):
                            continue
                    test = urlconf.resolve(test_url)
                    if test:
                        urls.append(test_url)
            except Resolver404:
                continue
    recursive_handler(all_urls)
    return render(request, 'shopapp/index.html', context={'items': urls})


class ProductsListView(ListView):
    queryset = Product.objects.filter(being_under_sanctions=False)
    template_name = 'shopapp/list_products.html'
    context_object_name = 'products'


class ProductDetailsView(DetailView):
    queryset = Product.objects.filter(being_under_sanctions=False)
    template_name = 'shopapp/products_details.html'
    context_object_name = 'product'


class OrdersListView(ListView):
    queryset = Order.objects.filter(is_archived=False).select_related('user').prefetch_related('products')
    template_name = 'shopapp/list_orders.html'
    context_object_name = 'orders'


class OrdersDetailsView(DetailView):
    queryset = Order.objects.filter(is_archived=False).select_related('user').prefetch_related('products')
    template_name = 'shopapp/order_details.html'
    context_object_name = 'order'


def upload_file(request: HttpRequest):
    MAX_SIZE_MB = 1
    MAX_SIZE_BYTES = MAX_SIZE_MB * 1024 * 1024
    if request.method == "POST":
        file = request.FILES.get('file')
        if file:
            logger.info(f'size {file.size}')
            if file.size > MAX_SIZE_BYTES:
                message = 'Файл слишком большой!'
            else:
                path = os.path.join(mysite.settings.UPLOADS_DIR, f"{uuid.uuid4()}{file.name}")
                with open(path, 'wb+') as file_path:
                    for chunk in file.chunks():
                        file_path.write(chunk)
                message = 'Файл загружен!'
        else:
            message = 'Файл не был загружен!'
        return render(request, 'shopapp/upload-file.html', context={'message': message})
    else:
        return render(request, 'shopapp/upload-file.html')


class ProductCreateView(PermissionRequiredMixin, CreateView):
    model = Product
    fields = ['name', 'description', 'price']
    template_name = 'shopapp/create-product.html'
    success_url = reverse_lazy('shopapp:list_products')

    permission_required = 'shopapp.add_product'

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        return HttpResponseForbidden('У вас недостаточно прав')

    def form_valid(self, form):
        form.instance.crated_by = self.request.user.profile
        return super().form_valid(form)


class OrderCreateView(CreateView):
    model = Product
    template_name = 'shopapp/create-order.html'
    success_url = reverse_lazy('shopapp:list_orders')


class ProductUpdateView(CanUpdateProductMixin, UpdateView):
    model = Product
    template_name = 'shopapp/update-product.html'
    fields = 'name', 'description', 'price', 'rating'
    success_url = reverse_lazy('shopapp:list_products')


class OrderUpdateView(UpdateView):
    model = Order
    template_name = 'shopapp/update-order.html'
    fields = 'address', 'promocode', 'user', 'products'
    success_url = reverse_lazy('shopapp:list_orders')


class ProductArchiveView(DeleteView):
    model = Product
    template_name = 'shopapp/archive-product.html'
    success_url = reverse_lazy('shopapp:list_products')

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.being_under_sanctions = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class OrderArchiveView(DeleteView):
    model = Order
    template_name = 'shopapp/archive-order.html'
    success_url = reverse_lazy('shopapp:list_orders')

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.is_archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


@method_decorator(user_passes_test(lambda u: u.is_staff, login_url='/accounts/login/'), name='dispatch')
class OrderExportView(View):

    def get(self, request):
        orders = Order.objects.all()
        result = [
            {
                'id': order.pk,
                'address': order.address,
                'promocode': order.promocode,
                'products': [product.pk for product in order.products.all()],
                'user': order.user.pk
            }
            for order in orders
        ]
        return JsonResponse({'orders': result})

from rest_framework import viewsets
from shopapp.serializers import OrderSerializer, ProductSerializer
from rest_framework.response import Response

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    search_fields = ['address', 'promocode']
    ordering_fields = ['address']

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'description', 'price']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(crated_by=request.user.profile)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)
