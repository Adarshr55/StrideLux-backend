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
from django.db import models as db_models
from utils.pagination import paginate_queryset
from django.db.models import Case, When, Value, IntegerField

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
        search = request.query_params.get('search', '')
        category = request.query_params.get('category', '')
        is_active = request.query_params.get('is_active', 'true')

        products=Product.objects.all().order_by('-created_at')
        if is_active == 'true':
            products = products.filter(is_active=True)
        else:
            products = products.filter(is_active=False)

        if search:
            products = products.filter(
                db_models.Q(name__icontains=search) |
                db_models.Q(brand__icontains=search)
            )
        if category and category != 'All':
            products = products.filter(category__name__iexact=category)
        
        result = paginate_queryset(products, request, page_size=8)

        serializer = ProductSerializer(
            result['queryset'], many=True, context={'request': request}
        )

        return Response({
            'results': serializer.data,
            **result['meta']     
        })
    
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
       
       search = request.query_params.get('search', '')
       is_active = request.query_params.get('is_active', 'true')

       users = User.objects.filter(is_admin=False).order_by('-created_at')

       if is_active == 'false':
            users = users.filter(is_active=False)
       else:
            users = users.filter(is_active=True)

       if search:
            users = users.filter(
                db_models.Q(username__icontains=search) |
                db_models.Q(email__icontains=search)
            )

       result = paginate_queryset(users, request, page_size=10)

       serializer = UserSerializer(result['queryset'], many=True)
       return Response({
            'results': serializer.data,
            **result['meta']
        })

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
        search = request.query_params.get('search', '')
        status_filter = request.query_params.get('status', '')

        orders = Order.objects.all().annotate(
            status_order=Case(
                When(status='pending', then=Value(1)),
                When(status='shipped', then=Value(2)),
                When(status='delivered', then=Value(3)),
                When(status='cancelled', then=Value(4)),
                default=Value(5),
                output_field=IntegerField(),
            )
        ).order_by('status_order', '-created_at')

        if search:
            orders = orders.filter(
                db_models.Q(id__icontains=search) |
                db_models.Q(user__username__icontains=search)
            )
        if status_filter and status_filter != 'All':
            orders = orders.filter(status=status_filter)

        result = paginate_queryset(orders, request, page_size=10)

        serializer = OrderSerializer(result['queryset'], many=True)
        return Response({
            'results': serializer.data,
            **result['meta']
        })
    
class AdminOrderDetailView(APIView):
    permission_classes=[IsAdminUser]

    def patch(self,request,pk):
        try:
            order = Order.objects.get(id=pk)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

        if order.status in ['delivered', 'cancelled']:
            return Response(
            {'error': 'Cannot change completed or cancelled orders'},
            status=status.HTTP_400_BAD_REQUEST
        )
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





        


    