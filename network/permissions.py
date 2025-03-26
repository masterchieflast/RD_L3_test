from rest_framework.permissions import BasePermission
from .models import Employee

class IsActiveEmployeePermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not (user and user.is_authenticated):
            return False
        return Employee.objects.filter(user=user, active=True).exists()
