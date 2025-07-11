from django.contrib import admin
from app1.models import Product
from django.contrib import admin
from .models import CustomUser

admin.site.register(CustomUser)
# Register your models here.
admin.site.register(Product)

