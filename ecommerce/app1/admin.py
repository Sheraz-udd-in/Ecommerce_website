from django.contrib import admin
from app1.models import Product
from django.contrib import admin
from .models import CustomUser,Cart,CartItem,Order

admin.site.register(CustomUser)
# Register your models here.
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(Product)

