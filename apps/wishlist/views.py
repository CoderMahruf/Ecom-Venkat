from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import Wishlist,WishlistProduct
from .serializers import WishlistSerializer
from apps.product.models import Product
# Create your views here.

class WishlistView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
        serializer = WishlistSerializer(wishlist)
        return Response({
            "status": "success",
            "message": "Wishlist data fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

class WishlistCreateView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            product_id = kwargs.get("product_id")
            product = get_object_or_404(Product, id=product_id)
            
            wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
            item, created = WishlistProduct.objects.get_or_create(wishlist=wishlist, product=product)

            if not created:
                item.delete()
                return Response({
                    "status": "success",
                    "message": "Wishlist item Successfully Deleted!",
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "status": "success",
                    "message": "Wishlist Successfully Created!",
                }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "status": "error",
                "message": "Unusual Error",
                "details": str(e),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




        