from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import WishlistItemSerializer
from .models import WishlistItem
from rest_framework.views import APIView
from products.models import Product
# Create your views here.
class Wishlistview(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request):
        item=WishlistItem.objects.filter(user=request.user)
        serializer=WishlistItemSerializer(item,many=True,context={'request': request})
        return Response(serializer.data)
    
class WishlistAddView(APIView):
    permission_classes=[IsAuthenticated]

    def post(self,request):
        product_id=request.data.get('product_id')

        try:
            product=Product.objects.get(id=product_id,is_active=True)
        except Product.DoesNotExist:
            return Response({'error':'Product not found'},status=status.HTTP_404_NOT_FOUND)
        
        if WishlistItem.objects.filter(user=request.user,product=product).exists():
            return Response({'error': 'Already in wishlist'},
                status=status.HTTP_400_BAD_REQUEST
                )
        
        item=WishlistItem.objects.create(user=request.user, product=product)

        serializer = WishlistItemSerializer(
            item, context={'request': request}
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class WishlistRemoveView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self,request,product_id):
        try:
            item = WishlistItem.objects.get(
                user=request.user,
                product_id=product_id
            )
            item.delete()
            return Response({'message': 'Removed from wishlist'},status=status.HTTP_204_NO_CONTENT)
        except WishlistItem.DoesNotExist:
            return Response(
                {'error': 'Item not found'},
                status=status.HTTP_404_NOT_FOUND
            )


