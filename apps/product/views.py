from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
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
