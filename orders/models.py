from django.db import models
from django.conf import settings
from  products.models import Product
# Create your models here.
class Order(models.Model):
      STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
      PAYMENT_CHOICES = [
        ('COD', 'Cash on Delivery'),
        ('CARD', 'Credit/Debit Card'),
        ('UPI', 'UPI'),
    ]
      user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='orders')
      status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='pending')
      total=models.DecimalField(max_digits=10,decimal_places=2)
      fullname=models.CharField(max_length=100)
      address=models.TextField()
      city=models.CharField(max_length=100)
      phone=models.CharField(max_length=15)
      payment=models.CharField(max_length=10,choices=PAYMENT_CHOICES,default='COD')
      razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
      razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
      is_paid = models.BooleanField(default=False)
      
      created_at=models.DateTimeField(auto_now_add=True)
      updated_at=models.DateTimeField(auto_now=True)



      def __str__(self):
        return f"Order #{self.id} by {self.user.email}"
    
class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items')
    product=models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    name=models.CharField(max_length=225)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    quantity=models.PositiveIntegerField()
    selected_size=models.CharField(max_length=500,null=True,blank=True)
    thumbnail=models.CharField(max_length=500,blank=True,null=True)

    def __str__(self):
        return f"{self.name}-{self.quantity}"
    
    @property
    def item_total(self):
        return float(self.price)*self.quantity
    
