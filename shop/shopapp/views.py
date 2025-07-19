from django.http import HttpResponse, HttpRequest
from django.shortcuts import render

from shopapp.models import Product, Order


def shop_index(request: HttpRequest) -> HttpResponse:
    context = {}
    return render(request, "shopapp/shop_index.html", context=context)


def products_list(request: HttpRequest) -> HttpResponse:
    context = {
        "products": Product.objects.all(),
    }
    return render(request, "shopapp/products_list.html", context=context)


def orders_list(request: HttpRequest) -> HttpResponse:
    context = {
        "orders": Order.objects.select_related("user").prefetch_related("products").all()
    }
    return render(request, "shopapp/orders_list.html", context=context)
