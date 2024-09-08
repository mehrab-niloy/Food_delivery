from rest_framework import permissions

class IsOwnerOrEmployee(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role in ['owner', 'employee']

    def has_object_permission(self, request, view, obj):
        return obj.restaurant == request.user.restaurant
