from django.urls import path
from .views import ConversationMessagesView

urlpatterns = [
    path('conversation/<int:conversation_id>/messages/', ConversationMessagesView.as_view(), name='conversation-messages'),
]
