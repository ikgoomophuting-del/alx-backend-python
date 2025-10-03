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
