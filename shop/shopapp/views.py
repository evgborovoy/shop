import logging
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from .serializers import ProductSerializer, OrderSerializer

from django_filters.rest_framework import DjangoFilterBackend

from shopapp.models import Product, Order

log = logging.getLogger(__name__)


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    search_fields = ["name", "description"]
    filterset_fields = [
        "name",
        "description",
        "price",
        "discount",
        "archived",
    ]
    ordering_fields = ["name", "price"]


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.select_related("user").prefetch_related("products").all()
    serializer_class = OrderSerializer
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
    ]
    search_fields = [
        "delivery_address",
        "promocode",
    ]
    filterset_fields = [
        "delivery_address",
        "promocode",
    ]


def shop_index(request: HttpRequest) -> HttpResponse:
    context = {}
    return render(request, "shopapp/shop_index.html", context=context)


class ProductsListView(ListView):
    queryset = Product.objects.filter(archived=False)
    context_object_name = "products"
    template_name = "shopapp/products_list.html"


class ProductDetailsView(DetailView):
    model = Product
    template_name = "shopapp/product_detail.html"


class ProductCreateView(CreateView):
    model = Product
    fields = ["name", "price", "description", "discount"]
    success_url = reverse_lazy("shopapp:products_list")
    template_name = "shopapp/create_product.html"


class ProductUpdateView(UpdateView):
    model = Product
    fields = ["name", "price", "description", "discount"]
    template_name = "shopapp/update_product.html"

    def get_success_url(self):
        return reverse(
            "shopapp:product_details",
            kwargs={"pk": self.object.pk},
        )


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("shopapp:products_list")

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class OrdersListView(LoginRequiredMixin, ListView):
    queryset = Order.objects.select_related("user").prefetch_related("products")
    context_object_name = "orders"
    template_name = "shopapp/orders_list.html"


class OrderDetailView(PermissionRequiredMixin, DetailView):
    permission_required = ["shopapp.view_order"]
    queryset = Order.objects.select_related("user").prefetch_related("products")


class OrderUpdateView(UpdateView):
    model = Order
    fields = ["delivery_address", "promocode", "products"]
    template_name = "shopapp/order_update.html"

    def get_success_url(self):
        return reverse(
            "shopapp:order_detail",
            kwargs={"pk": self.object.pk},
        )


class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy("shopapp:orders_list")


class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    fields = ["delivery_address", "promocode", "products"]
    success_url = reverse_lazy("shopapp:orders_list")
    template_name = "shopapp/create_order.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
