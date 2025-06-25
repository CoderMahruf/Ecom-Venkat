from rest_framework import serializers
from .models import Wishlist,WishlistProduct

class WishlistItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishlistProduct
        fields = ['id', 'wishlist', 'product']
        read_only_fields = ['id']

class WishlistSerializer(serializers.ModelSerializer):
    items = WishlistItemSerializer(many=True, read_only=True)

    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'created_at', 'items']
        read_only_fields = ['id']
