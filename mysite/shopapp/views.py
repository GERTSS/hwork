from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.urls import get_resolver, Resolver404

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


def list_products(request: HttpRequest):
    context = {
        'products': Product.objects.all()
    }
    return render(request, 'shopapp/list_products.html', context=context)


def list_orders(request: HttpRequest):
    context = {
        'orders': Order.objects.select_related('user').prefetch_related('products').all()
    }
    return render(request, 'shopapp/list_orders.html', context=context)


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


def create_product(request: HttpRequest):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_products')
        else:
            return render(request, 'shopapp/create-product.html',
                          context={'form': form, 'message': 'Не валидные данные'})
    else:
        form = ProductForm()
        return render(request, 'shopapp/create-product.html', context={'form': form})


def create_order(request: HttpRequest):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_products')
        else:
            return render(request, 'shopapp/create-order.html',
                          context={'form': form, 'message': 'Не валидные данные'})
    else:
        form = OrderForm()
        return render(request, 'shopapp/create-order.html', context={'form': form})
