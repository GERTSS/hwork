from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import get_resolver, Resolver404, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View

import mysite.settings
from shopapp.models import Product, Order
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


class ProductCreateView(CreateView):
    model = Product
    template_name = 'shopapp/create-product.html'
    success_url = reverse_lazy('list_products')


class OrderCreateView(CreateView):
    model = Product
    template_name = 'shopapp/create-order.html'
    success_url = reverse_lazy('list_orders')


class ProductUpdateView(UpdateView):
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
