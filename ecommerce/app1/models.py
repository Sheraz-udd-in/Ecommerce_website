from django.db import models
# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('vendor', 'Vendor'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')

class Product(models.Model) :
    name  =  models.CharField(max_length=100)
    des = models.TextField()
    price =  models.FloatField()
    created_at =  models.DateTimeField(auto_now_add=True)
    
