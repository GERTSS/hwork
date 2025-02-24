from django.shortcuts import render
from django.http import HttpRequest
from django.urls import get_resolver, Resolver404
from shopapp.models import Product, Order


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