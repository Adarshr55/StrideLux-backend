from django.shortcuts import render
from .serializers import OrderItemSerializer,OrderSerializer
from .models import Order,OrderItem
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from cart.models import Cart
import razorpay
from django.conf import settings
# Create your views here.
class OrderListView(APIView):
    permission_classes=[IsAuthenticated]


    def get(self,request):
        order=Order.objects.filter(user=request.user).order_by('-created_at')
        serializer=OrderSerializer(order,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        data=request.data
        try:
            cart=Cart.objects.get(user=request.user)
            cart_items=cart.items.all()
        except Cart.DoesNotExist:
            return Response( {'error': 'Cart is empty'},status=status.HTTP_400_BAD_REQUEST)
        
        if not cart_items.exists():
            return Response({'error':'Cart is empty'},status=status.HTTP_400_BAD_REQUEST)
        
        order=Order.objects.create(user=request.user,total=cart.items.count() and 
                sum(float(item.product.price)*item.quantity
                     for item in cart_items),
                      fullname=data.get('fullname', ''),
                      address=data.get('address', ''),
                      city=data.get('city', ''),
                      phone=data.get('phone', ''),
                      payment=data.get('payment', 'COD'),
                      status='pending'
                     )
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                name=item.product.name,
                price=item.product.price,
                quantity=item.quantity,
                selected_size=item.selected_size,
                 thumbnail=request.build_absolute_uri(
                    item.product.thumbnail.url
                )if item.product.thumbnail else None
            )

        cart.items.all().delete()

        serializer=OrderSerializer(order)
        return Response(serializer.data,status=status.HTTP_201_CREATED)


class OrderDetailView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request,pk):

        try:
            order=Order.objects.get(id=pk,user=request.user)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'},status=status.HTTP_404_NOT_FOUND)
        serializer=OrderSerializer(order)
        return Response(serializer.data)
    
    def patch(self,request,pk):

        try:
            order=Order.objects.get(id=pk,user=request.user)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'},status=status.HTTP_404_NOT_FOUND)
        
        if order.status not in ['pending','shipped']:
            return Response( {'error': 'Order cannot be cancelled'},
                status=status.HTTP_400_BAD_REQUEST)
        order.status='cancelled'
        order.save()
        serializer=OrderSerializer(order)
        return Response(serializer.data)
    
razorpay_client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)

class CreateRazorpayOrderView(APIView):
    permission_classes=[IsAuthenticated]

    def post(self,request,pk):
        try:
            order = Order.objects.get(id=pk, user=request.user)
        except Order.DoesNotExist:
            return Response(
                {'error': 'Order not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        if order.is_paid:
             return Response(
                {'error': 'Order already paid'},
                status=status.HTTP_400_BAD_REQUEST
            )
        amount = int(float(order.total) * 100)

        razorpay_order = razorpay_client.order.create({
            'amount': amount,
            'currency': 'INR',
            'receipt': f'order_{order.id}',
            'payment_capture': 1
        })

        order.razorpay_order_id = razorpay_order['id']
        order.save()
        return Response({
            'razorpay_order_id': razorpay_order['id'],
            'amount': amount,
            'currency': 'INR',
            'key': settings.RAZORPAY_KEY_ID,
            'order_id': order.id,
            'name': request.user.username,
            'email': request.user.email,
            'phone': order.phone,
        })
    
class VerifyPaymentView(APIView):
    permission_classes=[IsAuthenticated]

    def post(self, request, pk):
        try:
            order = Order.objects.get(id=pk, user=request.user)
        except Order.DoesNotExist:
            return Response(
                {'error': 'Order not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        razorpay_payment_id = request.data.get('razorpay_payment_id')
        razorpay_order_id = request.data.get('razorpay_order_id')
        razorpay_signature = request.data.get('razorpay_signature')

        try:
            razorpay_client.utility.verify_payment_signature({
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature,
            })
            order.razorpay_payment_id = razorpay_payment_id
            order.is_paid = True
            order.status = 'pending'
            order.save()

            return Response({'message': 'Payment verified successfully'})
        except razorpay.errors.SignatureVerificationError:
            return Response(
                {'error': 'Payment verification failed'},
                status=status.HTTP_400_BAD_REQUEST
            )
        



        

        