from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (shop_index,
                    ProductDetailsView,
                    ProductsListView,
                    OrdersListView,
                    OrderDetailView,
                    ProductCreateView,
                    ProductUpdateView,
                    ProductDeleteView,
                    OrderUpdateView,
                    OrderDeleteView,
                    OrderCreateView,
                    ProductViewSet,
                    OrderViewSet,
                    )

app_name = "shopapp"

routers = DefaultRouter()
routers.register("products", ProductViewSet)
routers.register("orders", OrderViewSet)

urlpatterns = [
    path("", shop_index, name="index"),
    path("api/", include(routers.urls)),
    path("products/", ProductsListView.as_view(), name="products_list"),
    path("products/<int:pk>/", ProductDetailsView.as_view(), name="product_detail"),
    path("products/<int:pk>/update/", ProductUpdateView.as_view(), name="product_update"),
    path("products/<int:pk>/archive/", ProductDeleteView.as_view(), name="product_delete"),
    path("products/create/", ProductCreateView.as_view(), name="create_product"),
    path("orders/", OrdersListView.as_view(), name="orders_list"),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="order_detail"),
    path("orders/<int:pk>/update/", OrderUpdateView.as_view(), name="order_update"),
    path("orders/<int:pk>/delete/", OrderDeleteView.as_view(), name="order_delete"),
    path("orders/create/", OrderCreateView.as_view(), name="create_order"),
]
