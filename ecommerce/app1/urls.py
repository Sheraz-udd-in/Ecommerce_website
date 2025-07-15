from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from  .views import products , product_detail , register_user

urlpatterns = [
    path('products/', products),
    path('products/<int:id>',  product_detail ),
    # add these views
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/' , register_user )


]