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
    Custom permission to allow only participants in a conversation
    to send, view, update, and delete messages.
    """

    def has_permission(self, request, view):
        # ✅ Ensure the user is authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Check if the logged-in user is a participant in the conversation
        related to the object (message or conversation).
        """
        if hasattr(obj, "conversation"):
            # obj is a Message instance
            return (
                request.user == obj.conversation.sender
                or request.user == obj.conversation.receiver
            )
        elif hasattr(obj, "sender") and hasattr(obj, "receiver"):
            # obj is a Conversation instance
            return request.user in [obj.sender, obj.receiver]
        return False
        
