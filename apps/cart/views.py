from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404

from .models import Cart, CartItems
from .serializers import CartSerializer, CartItemSerializer
from apps.product.models import Product
# Create your views here.

class UserCartView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddCartItemView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        data = request.data.copy()
        data['cart'] = cart.id
        serializer = CartItemSerializer(data=data)
        if serializer.is_valid():
            serializer.save(cart=cart)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteCartItemView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def delete(self, request, pk):
        cart = get_object_or_404(Cart, user=request.user)
        item = get_object_or_404(CartItems, pk=pk, cart=cart)
        item.delete()
        return Response({"message": "Item removed from cart."}, status=status.HTTP_204_NO_CONTENT)
