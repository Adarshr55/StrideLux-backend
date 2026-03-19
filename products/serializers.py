from rest_framework import serializers
from .models import Category,Product,ProductImage,Size

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['id','name','image']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductImage
        fields=['id','image']

class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Size
        fields=['id','size']

class ProductSerializer(serializers.ModelSerializer):
    category=CategorySerializer(read_only=True)
    thumbnail=serializers.ImageField(read_only=True)
    class Meta:
        model=Product
        fields=['id','name','brand','category','price','stock','rating','thumbnail','is_active']

class ProductDetailSerializer(serializers.ModelSerializer):
    category=CategorySerializer(read_only=True)
    images=ProductImageSerializer(many=True,read_only=True)
    sizes=SizeSerializer(many=True,read_only=True)

    class Meta:
        model=Product
        fields=['id','name','brand','category','description','price','stock','rating','thumbnail','images',
                'sizes','is_active','created_at']
