from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=100,unique=True)
    image=models.ImageField(upload_to='categories/',blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural='categories'

class Product(models.Model):
    category=models.ForeignKey(
        Category,on_delete=models.SET_NULL,null=True,related_name='products'
    )
    name=models.CharField(max_length=255)
    brand=models.CharField(max_length=100)
    description=models.TextField(blank=True,null=True)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    stock=models.PositiveIntegerField(default=0)
    rating=models.DecimalField(max_digits=3,decimal_places=2,default=0.0,validators=[MinValueValidator(0.0),MaxValueValidator(5.0)])
    thumbnail=models.ImageField(upload_to='thumbnails/',blank=True,null=True)
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='images')
    image=models.ImageField(upload_to='products/')

    def __str__(self):
        return f"{self.product.name} image"
    
class Size(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='sizes')
    size=models.CharField(max_length=10)

    def __str__(self):
        return f"{self.product.name}-{self.size}"

