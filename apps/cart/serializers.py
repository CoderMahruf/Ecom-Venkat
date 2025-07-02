from rest_framework import serializers
from .models import Cart, CartItems
from apps.product.models import Product  

class CartItemSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source='product.title', read_only=True)
    product_price = serializers.DecimalField(source='product.price', read_only=True, max_digits=10, decimal_places=2)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItems
        fields = ['id', 'product', 'product_title', 'product_price', 'quantity', 'size', 'total_price']

    def get_total_price(self, obj):
        return obj.get_total_price()

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True) 
    total_price = serializers.SerializerMethodField()
    total_offer_price = serializers.SerializerMethodField()
    discount = serializers.SerializerMethodField()
    final_price = serializers.SerializerMethodField()
    total_items = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = [
            'id', 'user', 'coupon', 'created_at',
            'items', 'total_price', 'total_offer_price',
            'discount', 'final_price', 'total_items'
        ]
        read_only_fields = ['user', 'created_at']

    def get_total_price(self, obj):
        return obj.get_total_price()

    def get_total_offer_price(self, obj):
        return obj.get_total_offer_price()

    def get_discount(self, obj):
        return obj.get_discount()

    def get_final_price(self, obj):
        return obj.get_total_price_after_discount()

    def get_total_items(self, obj):
        return obj.get_total_item_count()
