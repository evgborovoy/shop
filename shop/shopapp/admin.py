from django.contrib import admin
from .models import Product, Order


class OrderInline(admin.TabularInline):
    model = Product.orders.through


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        OrderInline
    ]
    list_display = ["pk", "name", "price", "description_short", "discount"]
    list_display_links = ["pk", "name"]
    ordering = ["-pk"]
    search_fields = ["name", "description"]
    fieldsets = [
        (None, {
            "fields": ("name", "description"),
        }),
        ("Price options", {
            "fields": ("price", "discount"),
        }),
        ("Options", {
            "fields": ("archived",),
            "classes": ("collapse",),
            "description": "Field 'archived' is for soft delete",
        }),
    ]


class ProductInline(admin.TabularInline):
    model = Order.products.through


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        ProductInline,
    ]
    list_display = ["user_verbose", "created_at", "promocode", "delivery_address"]

    def get_queryset(self, request):
        return Order.objects.select_related("user").prefetch_related("products")

    def user_verbose(self, obj: Order) -> str:
        return f"{obj.user.first_name} {obj.user.last_name}" or f"{obj.user.first_name}" or obj.user.username
