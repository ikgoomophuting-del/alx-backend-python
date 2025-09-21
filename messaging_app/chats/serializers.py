from rest_framework import serializers
from .models import User, Conversation, Message


# -------------------------------
# User Serializer
# -------------------------------
class UserSerializer(serializers.ModelSerializer):
    # Explicit password field for input (write-only)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "user_id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "role",
            "created_at",
            "password",
        ]
        read_only_fields = ["user_id", "created_at"]

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

    def validate_email(self, value):
        """Check that email is not empty."""
        if not value:
            raise serializers.ValidationError("Email cannot be empty")
        return value


# -------------------------------
# Message Serializer
# -------------------------------
class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField()  # Displays sender as string (email)

    class Meta:
        model = Message
        fields = [
            "message_id",
            "sender",
            "message_body",
            "sent_at",
        ]
        read_only_fields = ["message_id", "sent_at"]


# -------------------------------
# Conversation Serializer
# -------------------------------
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    # Explicitly use SerializerMethodField for nested messages
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            "conversation_id",
            "participants",
            "created_at",
            "messages",
        ]
        read_only_fields = ["conversation_id", "created_at"]

    def get_messages(self, obj):
        """Return all messages in this conversation."""
        messages = obj.messages.all()
        return MessageSerializer(messages, many=True).data
