from django.shortcuts import render
from django.http import HttpRequest


def index(request: HttpRequest):
    products = [('apple', 50), ('banana', 75), ('tomato', 25)]
    return render(request, 'shopapp/index.html', context={'items': products})
