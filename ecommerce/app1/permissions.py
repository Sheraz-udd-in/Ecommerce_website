# permissions.py
from rest_framework.permissions import BasePermission

class IsVendor(BasePermission):

    # overide the has permission function
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "vendor"