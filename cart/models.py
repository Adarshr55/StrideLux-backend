from django.db import models
from django.conf import settings
from products.models import Product
# Create your models here.
class Cart(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='cart')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"cart of {self.user.email}"


class CartItem(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='items')
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    selected_size=models.CharField(max_length=10,blank=True,null=True)
    
    def __str__(self):
        return f"{self.product.name}-{self.quantity}"
    
    @property
    def total_price(self):
        return float(self.product.price)*(self.quantity)