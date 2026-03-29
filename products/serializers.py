from rest_framework import serializers
from .models import Category,Product,ProductImage,Size

class CategorySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField() 
    class Meta:
        model=Category
        fields=['id','name','image']

    def get_image(self,obj):
        if obj.image:
            request=self.context.get('request')
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        
        first_product=obj.products.filter(is_active=True, thumbnail__isnull=False).first()

        if first_product and first_product.thumbnail:
                        request = self.context.get('request')
                        return request.build_absolute_uri(
                first_product.thumbnail.url
            ) if request else first_product.thumbnail.url
        return None



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
    thumbnail=serializers.SerializerMethodField()

    class Meta:
        model=Product
        fields=['id','name','brand','category','price','stock','rating','thumbnail','is_active','description','thumbnail']
    def get_thumbnail(self, obj):
        if not obj.thumbnail:
            return None
        thumbnail_str = str(obj.thumbnail)
        if thumbnail_str.startswith('http://') or thumbnail_str.startswith('https://'):
            return thumbnail_str
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.thumbnail.url)
        return obj.thumbnail.url


class ProductDetailSerializer(serializers.ModelSerializer):
    category=CategorySerializer(read_only=True)
    images=ProductImageSerializer(many=True,read_only=True)
    sizes=SizeSerializer(many=True,read_only=True)

    class Meta:
        model=Product
        fields=['id','name','brand','category','description','price','stock','rating','thumbnail','images',
                'sizes','is_active','created_at']
