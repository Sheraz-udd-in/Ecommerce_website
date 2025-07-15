from rest_framework.serializers import ModelSerializer

from .models import Product, CartItem, Order


class ProductSerializer(ModelSerializer) :
    class Meta :
        model  = Product
        fields = "__all__"



class CartItemSerializer(ModelSerializer) :
    class Meta  :
        model =  CartItem
        fields = "__all__"


class OrderSerializer(ModelSerializer) :
    class Meta :
        model =  Order ,
        fields =  "__all__"