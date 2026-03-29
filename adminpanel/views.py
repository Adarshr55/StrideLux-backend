from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from django.db.models.functions import TruncMonth
from django.contrib.auth import get_user_model
from .permission import IsAdminUser
from datetime import datetime
from django.db.models import Sum, Count
from products.models import Product,Category
from  orders.models import Order
from rest_framework.response import Response
from products.serializers import ProductSerializer,ProductDetailSerializer,CategorySerializer
from accounts.serializers import  UserSerializer
from orders.serializers import OrderSerializer
# Create your views here.
User=get_user_model()

class AdminStatsView(APIView):
    permission_classes=[IsAdminUser]

    def get(self,request):
        now=datetime.now()
        current_month=now.month
        current_year=now.year

        total_users=User.objects.filter(is_admin=False).count()
        total_products=Product.objects.filter(is_active=True).count()
        total_orders=Order.objects.count()
        total_revenue=Order.objects.filter(status='delivered').aggregate(total=Sum('total'))['total'] or 0

        pending=Order.objects.filter(status='pending').count()
        shipped=Order.objects.filter(status='shipped').count()
        delivered=Order.objects.filter(status='delivered').count()
        cancelled=Order.objects.filter(status='cancelled').count()

        monthly_orders=Order.objects.filter(
            created_at__month=current_month,
             created_at__year=current_year
            )
        monthly_revenue=monthly_orders.filter(status='delivered'
                ).aggregate(total=Sum('total'))['total'] or 0
        
        monthly_trend=[0]*12
        revenue_by_month=Order.objects.filter(
            status='delivered'
        ).annotate(
            month=TruncMonth('created_at')
        ).values('month').annotate(
            revenue=Sum('total')
        ).order_by('month')


        for entry in revenue_by_month:
            month_index=entry['month'].month-1
            monthly_trend[month_index]=float(entry['revenue'])

        return Response({
            'total_users': total_users,
            'total_products': total_products,
            'total_orders': total_orders,
            'total_revenue': float(total_revenue),
            'pending': pending,
            'shipped': shipped,
            'delivered': delivered,
            'cancelled': cancelled,
            'monthly_orders': monthly_orders.count(),
            'monthly_revenue': float(monthly_revenue),
            'monthly_delivered': monthly_orders.filter(status='delivered').count(),
            'monthly_pending': monthly_orders.filter(status='pending').count(),
            'monthly_shipped': monthly_orders.filter(status='shipped').count(),
            'monthly_cancelled': monthly_orders.filter(status='cancelled').count(),
            'revenue_trend': monthly_trend,
        })
    
class AdminProductListView(APIView):

    permission_classes=[IsAdminUser]

    def get(self,request):
        products=Product.objects.all().order_by('-created_at')
        serializer=ProductSerializer(products,many=True,context={'request':request})
        return Response(serializer.data)
    
    def post(self,request):
        category_name = request.data.get('category', '').lower()
        category, _ = Category.objects.get_or_create(name=category_name)

        product=Product.objects.create(
             name=request.data.get('name'),
             brand=request.data.get('brand'),
             category=category,
             description=request.data.get('description', ''),
             price=request.data.get('price'),
             stock=request.data.get('stock', 0),
             rating=request.data.get('rating', 0),
             is_active=True
        )
        if 'thumbnail' in request.FILES:
            product.thumbnail = request.FILES['thumbnail']
            product.save()

        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class AdminProductDetailView(APIView):
    permission_classes = [IsAdminUser]

    def put(self,request,pk):
        try:
            product = Product.objects.get(id=pk)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        
        category_name = request.data.get('category', '').lower()
        category, _ = Category.objects.get_or_create(name=category_name)

        product.name = request.data.get('name', product.name)
        product.brand = request.data.get('brand', product.brand)
        product.category = category
        product.description = request.data.get('description', product.description)
        product.price = request.data.get('price', product.price)
        product.stock = request.data.get('stock', product.stock)
        product.rating = request.data.get('rating', product.rating)
        thumbnail_url = request.data.get('thumbnail_url', '')
        if 'thumbnail' in request.FILES:
            product.thumbnail = request.FILES['thumbnail']

        product.save()

        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data)
    
    def patch(self,request,pk):

        try:
            product = Product.objects.get(id=pk)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        product.is_active = not product.is_active
        product.save()
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data)
    

class AdminUserListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        users = User.objects.filter(is_admin=False).order_by('-created_at')
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

class AdminUserBlockView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, pk):
        try:
            user = User.objects.get(id=pk, is_admin=False)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        user.is_active = not user.is_active 
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
class AdminUserBlockOnlyView(APIView):
    permission_classes=[IsAdminUser]

    def patch(self,request,pk):
        try:
            user=User.objects.get(id=pk,is_admin=False)
        except User.DoesNotExist:
            return Response({'error':"User not found"},status=status.HTTP_404_NOT_FOUND)
        user.is_blocked = not user.is_blocked
        user.save()
        serializer=UserSerializer(user)
        return Response(serializer.data)
    

class AdminOrderListview(APIView):
    permission_classes = [IsAdminUser]

    def get(self,request):
        order=Order.objects.all().order_by('-created_at')
        serializer=OrderSerializer(order,many=True)
        return Response(serializer.data)
    
class AdminOrderDetailView(APIView):
    permission_classes=[IsAdminUser]

    def patch(self,request,pk):
        try:
            order = Order.objects.get(id=pk)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        new_status = request.data.get('status')
        if new_status not in ['pending', 'shipped', 'delivered', 'cancelled']:
            return Response({'error': 'Invalid status'}, status=status.HTTP_404_NOT_FOUND)
          
        order.status = new_status
        order.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    
    def delete(self, request, pk):
        try:
            order = Order.objects.get(id=pk)
            order.delete()
            return Response({'message': 'Order deleted'})
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)





        


    