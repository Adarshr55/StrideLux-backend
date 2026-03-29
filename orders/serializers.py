from rest_framework import serializers
from .models import Order,OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    item_total=serializers.ReadOnlyField()

    class Meta:
        model=OrderItem
        fields=['id','name','price','quantity','selected_size','thumbnail','item_total']

class OrderSerializer(serializers.ModelSerializer):
    items=OrderItemSerializer(many=True,read_only=True)

    class Meta:
        model=Order
        fields=['id','status','total','fullname','address','city','phone','payment','items','created_at','is_paid','razorpay_order_id']
