from rest_framework.permissions import BasePermission


class UserPermissions(BasePermission):

    def has_permission(self, request, view):
        return request.user.groups.filter(name="moders").exists()


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True
        return False
