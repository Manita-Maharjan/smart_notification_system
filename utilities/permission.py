from rest_framework import permissions

from accounts.models import User

class IsSuperUser(permissions.BasePermission):
    """
    Check if user is superuser
    """
    message = 'Only superadmin is allowed'

    def has_permission(self, request, view):
        return request.user.is_superuser

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Write permissions are only allowed to the owner

        if hasattr(obj, 'user'):
            return obj.user == request.user
        elif isinstance(obj, User): 
            return obj.id == request.user.id
        return False
    
        


