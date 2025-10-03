from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Message
from .serializers import MessageSerializer


class MessageListCreateView(generics.ListCreateAPIView):
    """
    List all messages or create a new one.
    Supports parent_message for threaded replies.
    """
    queryset = Message.objects.all().select_related(
        "sender", "receiver", "parent_message"
    ).prefetch_related("replies")
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically set the sender as the logged-in user
        serializer.save(sender=self.request.user)


class ConversationView(APIView):
    """
    Retrieve a threaded conversation between the logged-in user and another user.
    Returns messages with nested replies.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, user_id, *args, **kwargs):
        other_user = get_object_or_404(User, id=user_id)

        # Top-level messages (not replies) between the two users
        messages = Message.objects.filter(
            sender__in=[request.user, other_user],
            receiver__in=[request.user, other_user],
            parent_message__isnull=True
        ).select_related("sender", "receiver") \
         .prefetch_related("replies__sender", "replies__receiver")

        data = []
        for msg in messages:
            data.append({
                "id": msg.id,
                "sender": msg.sender.username,
                "receiver": msg.receiver.username,
                "content": msg.content,
                "timestamp": msg.timestamp,
                "replies": msg.get_thread()  # recursive threaded replies
            })

        return Response(data, status=status.HTTP_200_OK)
