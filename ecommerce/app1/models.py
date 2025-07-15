from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('vendor', 'Vendor'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')


class Product(models.Model):
    name = models.CharField(max_length=100)
    des = models.TextField()
    price = models.FloatField()
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    vendor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.username}'s Cart"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in {self.cart.user.username}'s cart"


class Order(models.Model) :
    status_choices  = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('shipped' ,  'shipped') ,
        ('delivered' ,  'Delivered') ,
        ('canceled' ,  'Canceled')
    )
    product  =  models.ForeignKey(Product , on_delete=models.CASCADE)
    quantity  =  models.PositiveIntegerField(default=1)
    purchase_price  =  models.FloatField()
    vendor  =  models.ForeignKey(CustomUser , on_delete=models.CASCADE)
    status  =  models.CharField(max_length=50 ,  default='pending' , choices= status_choices)
    created_at  =  models.DateTimeField(auto_now_add=True)