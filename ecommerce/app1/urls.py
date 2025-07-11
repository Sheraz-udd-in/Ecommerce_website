from django.urls import path, include
from rest_framework_simplejwt.views import ( TokenObtainPairView ,TokenRefreshView)
from  .views import *
urlpatterns = [
    path('product/', products ),
    path('product/<int:id>' ,  product_detail),
    path('product/<int:id>/update', product_update),
    path('product/<int:id>/delete',product_delete),
    # add these views
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Login
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh

]