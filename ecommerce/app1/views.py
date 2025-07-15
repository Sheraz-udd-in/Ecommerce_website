import json
import math

from django.core.cache import cache
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Product, Cart, CartItem, Order
from .permissions import IsVendor
from .serializer import ProductSerializer, CartItemSerializer, OrderSerializer
from django.contrib.auth import get_user_model

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def products(request):
    if request.method == 'GET':
        # Generate a unique cache key based on query parameters
        name = request.GET.get('name', '')
        max_price = request.GET.get('max_price', '')
        order = request.GET.get('order', '')
        page = request.GET.get('page', '1')
        cache_key = f"products:name={name}&max_price={max_price}&order={order}&page={page}"
        cached_response = cache.get(cache_key)

        if cached_response:
            return Response(cached_response)

        # DB query if not cached
        data = Product.objects.all()
        if name:
            data = data.filter(name__icontains=name)

        if max_price:
            data = data.filter(price__lte=max_price)

        if order:
            data = data.order_by(order)

        paginator = PageNumberPagination()
        paginator.page_size = 3
        result_page = paginator.paginate_queryset(data, request)
        serializer = ProductSerializer(result_page, many=True)
        response_data = paginator.get_paginated_response(serializer.data).data

        # Store in cache
        cache.set(cache_key, response_data, timeout=60 * 5)  # 5 minutes

        return Response(response_data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def product_detail(request  , id) :
    product = get_object_or_404(Product, id=id)
    if request.method == 'GET' :
        serializer  = ProductSerializer(product)
        return Response(serializer.data , status =  status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsVendor])
def create_product(request) :
    if request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Optional: clear relevant cache if needed
            cache.clear()
            return Response({"message": "success"}, status=status.HTTP_201_CREATED)
        return Response({"message": "Invalid format"}, status=status.HTTP_400_BAD_REQUEST)


# Path variable
@api_view(['POST' , 'PUT' , 'PATCH'])
@permission_classes([IsVendor])
def update_products(request , id) :
    product = get_object_or_404(Product, id=id)
    if request.method == 'DELETE' :
        product.delete()
        return Response({"message" : "deletion Success"} , status =  status.HTTP_204_NO_CONTENT)

    if request.method == 'PUT' :
        serializer   =  ProductSerializer(product ,  data  = request.data)
        if serializer.is_valid() :
            serializer.save()
            return  Response({"message" : "success"}  , status = status.HTTP_200_OK)
        return  Response({"message" : "Invalid format"} ,  status=status.HTTP_400_BAD_REQUEST)


    if request.method == 'PATCH':
        serializer =  ProductSerializer(product ,  data  = request.data , partial = True)
        if serializer.is_valid() :
            serializer.save()
            return Response({"message": "success"}, status=status.HTTP_200_OK)
        return  Response({"message" : "Invalid format"} ,  status=status.HTTP_400_BAD_REQUEST)







User = get_user_model()


@api_view(['POST'])
@permission_classes([]) # this is a public view
def register_user(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if not username or not email or not password:
        raise ValidationError("Username, email, and password are required.")

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

    user = User(username=username, email=email)
    user.set_password(password)
    user.save()

    cart =  Cart(user =  user)
    cart.save()
    return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)


# cart views
from django.http import JsonResponse
@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def cart(request, id=None):
    user = request.user
    cart  = Cart.objects.filter(user=user).first()
    if request.method == "POST":
        quantity = request.GET.get('quantity', 1)
        product = get_object_or_404(Product, id=id)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        cart_item.quantity = quantity
        cart_item.save()

    if request.method == "DELETE":
        product = get_object_or_404(Product, id=id)
        cart_item = CartItem.objects.filter(cart=cart, product=product).first()
        if cart_item:
            cart_item.delete()


    cart_items = CartItem.objects.filter(cart=cart)
    serializer = CartItemSerializer(cart_items, many=True)

    # Billing logic
    total = 0
    for item in cart_items:
        total += item.product.price * int(item.quantity)
    total_with_tax_and_shipping = total + (total * 0.18) + 100  # 18% tax + flat ₹100 shipping

    return Response({
        "cart_items": serializer.data,
        "total_amount": round(total_with_tax_and_shipping, 2)
    })


# orders

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def purchase(request) :
    user  =  request.user
    cart = get_object_or_404(Cart , user  =  user)
    cart_items = CartItem.objects.filter(cart=cart)
    for i  in cart_items :
        order = Order(product  =  i.product , quantity =  i.quantity ,  purchase_price =  i.product.price ,  vendor  =  i.product.vendor)
        order.save()
    cart_items.delete()
    return  Response({"message" : "purchase sucessfull"})

# GET order ? status=pending

@api_view(['GET'])
@permission_classes([IsVendor])
def orders(request) :
    vendor = request.user
    status  =  request.GET.get('status')
    order  = Order.objects.filter(vendor  = vendor).order_by('-created_at')

    if status :
        order  =  order.filter(status =  status)

    serializer  = OrderSerializer(order ,  many=True)

    return Response(serializer.data  , status = status.HTTP_200_OK )


@api_view(['GET' , 'PATCH' ])
@permission_classes([IsVendor])
def order_detail(request  , id) :
    if  request.method  == "GET" :
        order =  get_object_or_404(Order , id  = id)
        if  order.vendor != request.user :
            return Response({"message" : "Unauthorized"} , status =  status.HTTP_401_UNAUTHORIZED)

        serializer  = OrderSerializer(order)

        return Response(serializer.data  ,status =  status.HTTP_200_OK )


    if request.method == "PATCH" :
        order = get_object_or_404(Order, id=id)
        if order.vendor != request.user:
            return Response({"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        data  =  request.data

        serializer  = OrderSerializer(order ,  data =  data  ,  partial=True)

        if serializer.is_valid() :
            serializer.save()

        return  Response(serializer.data  ,  status = status.HTTP_200_OK)