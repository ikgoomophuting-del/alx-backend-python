
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


# -------------------------------
# Custom User Model
# -------------------------------
class User(AbstractUser):
    """
    Extended User model based on Django's AbstractUser.
    Adds fields from the specification: UUID, phone_number, role, timestamps.
    """

    # Override default ID with UUID
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Email as unique identifier
    email = models.EmailField(unique=True, null=False)

    # Extra fields
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    ROLE_CHOICES = [
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='guest')

    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']  # keep username for Django admin

    def __str__(self):
        return f"{self.email} ({self.role})"


# -------------------------------
# Conversation Model
# -------------------------------
class Conversation(models.Model):
    """
    Conversation tracks participants (many-to-many with users).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(User, related_name="conversations")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.id} with {self.participants.count()} participants"


# -------------------------------
# Message Model
# -------------------------------
class Message(models.Model):
    """
    Messages belong to a Conversation and are linked to a sender.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages"
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_messages"
    )
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.email} at {self.sent_at}"
