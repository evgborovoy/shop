from rest_framework import serializers

from .models import Product, Order


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["pk", "name", "price", "discount", "description", "archived"]


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["pk", "delivery_address", "user", "created_at", "promocode", "products"]
