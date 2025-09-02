from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """Permission for Admin users only"""
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'Admin'

class IsManagerOrAdmin(permissions.BasePermission):
    """Permission for Manager and Admin users"""
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['Admin', 'Manager']

class IsSameBranchOrAdmin(permissions.BasePermission):
    """Permission for same branch users or Admin"""
    
    def has_permission(self, request, view):
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'Admin':
            return True
        
        # Check if object has branch attribute
        if hasattr(obj, 'branch'):
            return obj.branch == request.user.branch
        elif hasattr(obj, 'warehouse') and hasattr(obj.warehouse, 'branch'):
            return obj.warehouse.branch == request.user.branch
        
        return False
