from rest_framework.permissions import BasePermission
from .models import Employee


class IsActiveEmployeePermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not (user and user.is_authenticated):
            return False
        return Employee.objects.filter(user=user, active=True).exists()


class IsOwnerNetworkObject(BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            employee = request.user.employee
        except Employee.DoesNotExist:
            return False
        return obj.id == employee.network_object.id
