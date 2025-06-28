from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Banner,Category,Product
from .serializers import BannerSerializer,CategorySerializer,ProductSerializer
# Create your views here.
    
class BannerView(APIView):
    def get(self,request,*args, **kwargs):
        queryset = Banner.objects.all()
        serializer = BannerSerializer(queryset,many=True).data
        return Response({
            "status": "success",
            "message": "Banner data fetched successfully",
            "data": serializer
        }, status=status.HTTP_200_OK)
    
class CategoryView(APIView):
    def get(self,request,*args, **kwargs):
        queryset = Category.objects.all()
        serializer = CategorySerializer(queryset,many=True).data
        return Response({
            "status":"success",
            "message":"Category data fetched successfully",
            "data":serializer
        },status=status.HTTP_200_OK)
    

class ProductView(APIView):
    def get(self,request,*args, **kwargs):
        queryset = Product.objects.all()
        serializer = ProductSerializer(queryset,many=True).data
        return Response({
            "status":"success",
            "message":"Product data fetched successfully",
            "data":serializer
        },status=status.HTTP_200_OK)
    

class ProductCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "Product created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "success": "failed",
            "message": "Product creation failed",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailView(APIView):
    def get(self, request, product_id):
        try:
            product = Product.objects.prefetch_related(
                'images',
                'variants__color',
                'variants__size'
            ).get(pk=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        product_serializer = ProductSerializer(product)
        return Response({
            "product": product_serializer.data,
        })