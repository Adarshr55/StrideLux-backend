from django.shortcuts import render
from .models import Cart,CartItem
from .serializers import CartItemSerializer,CartSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from products.models import Product
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.

class CartView(APIView):
    permission_classes=[IsAuthenticated]
    
    def get(self,request):
        cart,_=Cart.objects.get_or_create(user=request.user)
        serializer=CartSerializer(cart,context={'request':request})
        return Response(serializer.data)
    
    def delete(self,request):
        cart,_=Cart.objects.get_or_create(user=request.user)
        cart.items.all().delete()
        return Response({'message':'cart cleared!'},status=status.HTTP_204_NO_CONTENT)
    
class CartItemView(APIView):
    permission_classes=[IsAuthenticated]


    def post(self,request):
        product_id=request.data.get('product_id')
        quantity=request.data.get('quantity',1)
        selected_size=request.data.get('selected_size')

        try:
            product=Product.objects.get(id=product_id,is_active=True)
        except Product.DoesNotExist:
            return Response({'error':'Product not found'},status=status.HTTP_404_NOT_FOUND)
        
        cart,_=Cart.objects.get_or_create(user=request.user)

        existing_item=cart.items.filter(product=product,selected_size=selected_size).first()

        if existing_item:
            existing_item.quantity +=quantity
            existing_item.save()

        else:
              CartItem.objects.create(
                cart=cart,
                product=product,
                quantity=quantity,
                selected_size=selected_size
            )
        serializer=CartSerializer(cart,context={'request':request})
        return Response(serializer.data,status=status.HTTP_200_OK)
    

class CartItemUpdateView(APIView):
    permission_classes=[IsAuthenticated]

    def patch(self, request, pk):
        try:
            cart = Cart.objects.get(user=request.user)
            item = cart.items.get(id=pk)
        except (Cart.DoesNotExist, CartItem.DoesNotExist):
            return Response(
                {'error': 'Item not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        quantity = request.data.get('quantity')
        if quantity is not None:
             
             quantity = int(quantity)
             if quantity <=0:
                 item.delete()
                 serializer = CartSerializer(cart, context={'request': request})
                 return Response(serializer.data)
             item.quantity =quantity
             item.save()

        serializer = CartSerializer(cart, context={'request': request})
        return Response(serializer.data)
    
    def delete(self, request, pk):
        try:
             cart = Cart.objects.get(user=request.user)
             item = cart.items.get(id=pk)
             item.delete()
        except(Cart.DoesNotExist, CartItem.DoesNotExist):
            return Response(
                {'error': 'Item not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = CartSerializer(cart, context={'request': request})
        return Response(serializer.data)
    


    
  
