from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    products,
    product_detail,
    create_product,
    update_products,
    register_user,
    cart,
    purchase,
    orders,
    order_detail,
)

urlpatterns = [

    path('register/', register_user),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    path('products/', products),  # GET
    path('products/<int:id>/', product_detail),  # GET
    path('products/create/', create_product),  # POST
    path('products/update/<int:id>/', update_products),  # PUT/PATCH/DELETE


    path('cart/', cart),  # GET cart, billing summary
    path('cart/<int:id>/', cart),  # POST (add), DELETE (remove item)


    path('purchase/', purchase),  # GET to create orders from cart


    path('orders/', orders),  # GET list of orders for vendor
    path('orders/<int:id>/', order_detail),  # GET, PATCH for a specific order
]