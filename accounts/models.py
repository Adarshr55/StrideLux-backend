from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
# Create your models here.

class UserManager(BaseUserManager):

    def create_user(self,email,password=None,**extra_fields):
        if not email:
            raise ValueError('email is required')
        email=self.normalize_email(email)
        user=self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_admin',True)
        return self.create_user(email,password,**extra_fields)
    
class User(AbstractUser):
    email=models.EmailField(unique=True)
    is_admin=models.BooleanField(default=False)
    phone=models.CharField(max_length=15,blank=True,null=True)
    address=models.TextField(blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username']

    objects=UserManager()

    groups=models.ManyToManyField(
        'auth.Group',
        related_name='accounts_users',
        blank=True
    )
    user_permissions=models.ManyToManyField(
        'auth.Permission',
        related_name='accounts_users',
        blank=True

    )

    def __str__(self):
        return self.email
