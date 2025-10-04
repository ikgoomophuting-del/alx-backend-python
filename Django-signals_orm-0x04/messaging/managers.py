from django.db import models

class UnreadMessagesManager(models.Manager):
    def unread_for_user(self, user):
        """
        Return unread messages for a specific receiver
        and optimize query with `.only()`.
        """
        return self.filter(receiver=user, read=False).only(
            "id", "sender", "receiver", "content", "timestamp", "parent_message"
        )
