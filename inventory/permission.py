from rest_framework import permissions


class IsEquipmentManager(permissions.BasePermission):
    """
    Custom permission to only allow equipment managers to access certain views.
    """

    def has_permission(self, request, view):

        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated  # Allow read-only access for any authenticated user
        # Check if the user is authenticated and has the 'equipment_manager' role
        return request.user and request.user.is_authenticated and request.user.role == 'VENDOR'
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any authenticated user,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated

        # Write permissions are only allowed to the equipment manager who owns the object.
        return obj.vendor == request.user