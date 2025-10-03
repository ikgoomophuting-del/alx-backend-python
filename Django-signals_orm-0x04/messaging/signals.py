from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Message, MessageHistory

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """
    Before saving, if the Message already exists and content is changed,
    log the old content into MessageHistory.
    """
    if instance.pk:  # message exists (not a new message)
        try:
            old_message = Message.objects.get(pk=instance.pk)
        except Message.DoesNotExist:
            return  # message doesn’t exist yet

        if old_message.content != instance.content:
            # Log old content
            MessageHistory.objects.create(
                message=instance,
                old_content=old_message.content
            )
            # Mark message as edited
            instance.edited = True
---

from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory

@receiver(post_delete, sender=User)
def cleanup_user_related_data(sender, instance, **kwargs):
    """
    When a user is deleted, remove related messages, notifications, and histories.
    """
    # Delete messages where user was sender or receiver
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    # Delete notifications for the user
    Notification.objects.filter(user=instance).delete()

    # Delete message histories linked to deleted user's messages
    MessageHistory.objects.filter(message__sender=instance).delete()
    MessageHistory.objects.filter(message__receiver=instance).delete()
        
