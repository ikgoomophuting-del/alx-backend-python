from django.db import models
from django.contrib.auth.models import User


class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        """
        Return unread messages for a specific user (receiver) 
        and only fetch necessary fields for efficiency.
        """
        return self.filter(receiver=user, read=False).only(
            "id", "sender", "content", "timestamp", "parent_message"
        )


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    # For edits
    edited = models.BooleanField(default=False)
    edited_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="edited_messages",
        help_text="The user who last edited this message."
    )

    # Threading
    parent_message = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="replies",
        help_text="If this message is a reply, link to the parent message."
    )

    # Read/unread tracking
    read = models.BooleanField(default=False)

    # Custom managers
    objects = models.Manager()  # default manager
    unread_messages = UnreadMessagesManager()  # custom manager for unread messages

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver} at {self.timestamp}"

    def get_thread(self):
        """
        Recursively fetch all replies to this message in threaded format.
        """
        thread = []
        for reply in self.replies.all().select_related("sender", "receiver").prefetch_related("replies"):
            thread.append({
                "id": reply.id,
                "sender": reply.sender.username,
                "content": reply.content,
                "timestamp": reply.timestamp,
                "replies": reply.get_thread()
            })
        return thread


class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="history")
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History for Message ID {self.message.id} at {self.edited_at}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="notifications")
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username} on message {self.message.id}"
