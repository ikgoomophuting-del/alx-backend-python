# messaging_app/chats/permissions.py
from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Only allow users to access their own objects.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

# messaging_app/chats/permissions.py
from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission:
    - Only authenticated users may access
    - Only participants of a conversation can view, send, update, or delete messages
    """

    def has_permission(self, request, view):
        # Ensure the user is logged in
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Restrict object-level permissions to conversation participants.
        """
        # Handle messages tied to conversations
        if hasattr(obj, "conversation"):
            participants = [obj.conversation.sender, obj.conversation.receiver]

        # Handle direct conversation objects
        elif hasattr(obj, "sender") and hasattr(obj, "receiver"):
            participants = [obj.sender, obj.receiver]

        else:
            return False  # object not recognized

        # Read permissions (GET, HEAD, OPTIONS) allowed for participants only
        if request.method in permissions.SAFE_METHODS:
            return request.user in participants

        # Unsafe methods (PUT, PATCH, DELETE, POST) also restricted to participants
        if request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            return request.user in participants

        return False
