# messaging_app/chats/permissions.py
from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Only allow users to access their own objects.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
