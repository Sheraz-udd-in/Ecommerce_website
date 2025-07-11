import json
import math
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from app1.permissions import IsVendor
from .models import Product
from .serializers import ProductSerializer
from django.core.paginator import Paginator
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

# REST API's
@permission_classes([IsAuthenticated, IsVendor])
@api_view(['GET', 'POST'])
def products(request):
    if request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.clear()
            return Response({'message': "success"}, status=status.HTTP_200_OK)
        return Response({'message': "failure", 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# filtering and searching  api response
#http://127.0.0.2:9000/api/product?max_price=1000
#http://127.0.0.2:9000/api/product?order=price or name
#http://127.0.0.2:9000/api/product?name=abc
    if request.method == 'GET' :
        name  =  request.GET.get('name')
        min_price =  request.GET.get('min_price')
        max_price =  request.GET.get('max_price')
        order = request.GET.get('order')
        page = int(request.GET.get('page',1))
        cache_key = f"products:name={name}&max_price={max_price}&order={order}&page={page}"
        cached_response = cache.get(cache_key)

        if cached_response:
            return Response(cached_response)
        
        products =  Product.objects.all()
        if name  : # we can fetch the data by name or by charcater
            products = Product.filter(name__icontains=name)
        if min_price : #we can set the value for which we want to see the price
            products =  products.filter(price__gte = min_price)

        if max_price : #we can set the value for which we want to see the price
            products = products.filter(price__lte = max_price)

        if  order : # we can order it according to our needs
            products =  products.order_by(order)
        # size = len(data)
        # page_size = 3
        # no_of_pages = math.ceil(size/page_size)
        # data = data[:3]
        # paginated_response = Paginator(products, per_page =3)
        # products = paginated_response.page(page)
        paginator = PageNumberPagination()
        paginator.page_size = 3
        result_page = paginator.paginate_queryset(products, request)
        serializer = ProductSerializer(result_page, many=True)
        response_data = paginator.get_paginated_response(serializer.data).data

        # Store in cache
        cache.set(cache_key, response_data, timeout=60 * 5)  # 5 minutes

        return Response(response_data)

@api_view(['GET'])
def product_detail(request,id):
    product=get_object_or_404(Product,id=id)
    serializer=ProductSerializer(product)
    return Response(serializer.data,status=status.HTTP_200_OK)
#update
@api_view(['PUT','PATCH'])
def product_update(request,id):
    product=get_object_or_404(Product,id=id)
    partial= True if request.method=='PATCH' else False
    serializer=ProductSerializer(product,data=request.data,partial=partial)
    if serializer.is_valid():
        serializer.save()
        return Response({'message':'Product updated successfully'},status=status.HTTP_200_OK)
    return Response({'message':'Product update failed'},status=status.HTTP_400_BAD_REQUEST)

#delete
@api_view(['DELETE'])
def product_delete(request,id):
    product=get_object_or_404(Product,id=id)
    product.delete()
    return Response({'message':'Product deleted Successfully'},status=status.HTTP_200_OK)

from rest_framework.views import APIView
from rest_framework.response import Response
from .permissions import IsVendor

class VendorOnlyView(APIView):
    permission_classes = [IsVendor]

    def get(self, request):
        return Response({"message": "Hello, Vendor!"})

