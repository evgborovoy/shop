from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from shopapp.models import Product, Order
from shopapp.forms import OrderForm


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


class OrdersListView(ListView):
    queryset = Order.objects.select_related("user").prefetch_related("products")
    context_object_name = "orders"
    template_name = "shopapp/orders_list.html"


class OrderDetailView(DetailView):
    queryset = Order.objects.select_related("user").prefetch_related("products")


@login_required
def create_order(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            form.save_m2m()
            url = reverse("shopapp:orders_list")
            return redirect(url)
    else:
        form = OrderForm()
    context = {
        "form": form
    }
    return render(request, "shopapp/create_order.html", context=context)
