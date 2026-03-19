from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from rest_framework.generics import ListAPIView,RetrieveAPIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from .models import Product,ProductImage,Category,Size
from .serializers import (CategorySerializer,ProductImageSerializer,
        ProductDetailSerializer,
        SizeSerializer,
        ProductSerializer
        )

# Create your views here.
class CategoryListView(ListAPIView):
    permission_classes=[AllowAny]
    queryset=Category.objects.all()
    serializer_class=CategorySerializer

class ProductListView(APIView):
    permission_classes=[AllowAny]
    def get(self,request):
        products=Product.objects.filter(is_active=True)

        search=request.query_params.get('search')
        if search:
             products=products.filter(Q(name__icontains=search)|Q(brand__icontains=search)|Q(description__icontains=search))

        category = request.query_params.get('category')
        if category:
            products = products.filter(category__name__icontains=category)
        serializer=ProductSerializer(products,many=True,context={'request':request})
        return Response(serializer.data)

class ProductDetailsView(RetrieveAPIView):
    permission_classes=[AllowAny]
    serializer_class=ProductDetailSerializer
  
    def get_queryset(self):
        return Product.objects.filter(is_active=True)
