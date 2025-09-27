awwfrom rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer


# -------------------------------
# Conversation ViewSet
# -------------------------------
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["participants__email"]  # allow filtering by participant email

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation with a list of participant IDs.
        Example payload:
        {
            "participants": ["uuid1", "uuid2"]
        }
        """
        participant_ids = request.data.get("participants", [])
        if not participant_ids:
            return Response(
                {"error": "At least one participant is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        conversation = Conversation.objects.create()
        conversation.participants.set(User.objects.filter(user_id__in=participant_ids))
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["get"])
    def messages(self, request, pk=None):
        """Custom endpoint: Get all messages in a conversation"""
        conversation = self.get_object()
        messages = conversation.messages.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


# -------------------------------
# Message ViewSet
# -------------------------------
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["message_body", "sender__email"]

    def create(self, request, *args, **kwargs):
        """
        Send a message to an existing conversation.
        Example payload:
        {
            "conversation_id": "uuid",
            "sender_id": "uuid",
            "message_body": "Hello world!"
        }
        """
        conversation_id = request.data.get("conversation_id")
        sender_id = request.data.get("sender_id")
        message_body = request.data.get("message_body")

        if not conversation_id or not sender_id or not message_body:
            return Response(
                {"error": "conversation_id, sender_id, and message_body are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        conversation = get_object_or_404(Conversation, conversation_id=conversation_id)
        sender = get_object_or_404(User, user_id=sender_id)

        message = Message.objects.create(
            conversation=conversation,
            sender=sender,
            message_body=message_body,
        )

        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# messaging_app/chats/views.py
from rest_framework import viewsets, permissions
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for conversations.
    Only participants can access, update, or delete.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        # Return only conversations the user is part of
        user = self.request.user
        return Conversation.objects.filter(sender=user) | Conversation.objects.filter(receiver=user)


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for messages.
    Only participants of the conversation can send, view, update, or delete messages.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        # Filter messages by user’s conversations
        user = self.request.user
        return Message.objects.filter(conversation__sender=user) | Message.objects.filter(conversation__receiver=user)

    def perform_create(self, serializer):
        # Ensure only participants can send messages
        conversation = serializer.validated_data["conversation"]
        if self.request.user not in [conversation.sender, conversation.receiver]:
            # DRF automatically raises 403 when permission check fails
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You are not a participant in this conversation.")

        serializer.save(sender=self.request.user)

from rest_framework import status

status.HTTP_403_FORBIDDEN  # => 403
