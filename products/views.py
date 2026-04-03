from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from rest_framework.generics import ListAPIView,RetrieveAPIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from .models import Product,ProductImage,Category,Size
from utils.pagination import paginate_queryset
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

    def get_serializer_context(self):
        return {'request':self.request}

class ProductListView(APIView):
    permission_classes=[AllowAny]
    def get(self,request):
        products=Product.objects.filter(is_active=True).order_by('created_at')

        search=request.query_params.get('search',"")
        if search:
             products=products.filter(Q(name__icontains=search)|Q(brand__icontains=search)|Q(description__icontains=search))

        category = request.query_params.get('category','')
        if category:
            products = products.filter(category__name__iexact=category)

        sort=request.query_params.get('sort','')
        if sort == 'priceLowHigh':
            products = products.order_by('price')
        elif sort == 'priceHighLow':
            products = products.order_by('-price')
        elif sort == 'nameAz':
            products = products.order_by('name')


        result = paginate_queryset(products, request, page_size=12)
        
        serializer=ProductSerializer( result['queryset'],many=True,context={'request':request})
        return Response({
            'results': serializer.data,
            **result['meta']
        })

class ProductDetailsView(RetrieveAPIView):
    permission_classes=[AllowAny]
    serializer_class=ProductDetailSerializer
  
    def get_queryset(self):
        return Product.objects.filter(is_active=True)
    

    def get_serializer_context(self): 
        return {'request': self.request}
