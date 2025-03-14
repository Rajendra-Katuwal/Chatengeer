from django.urls import path
from .views import ConversationCreateView, MessageCreateView, MessageListView

urlpatterns = [
    path('conversation/create/', ConversationCreateView.as_view(), name='conversation-create'),
    path('message/send/', MessageCreateView.as_view(), name='message-send'),
    path('messages/<int:conversation_id>/', MessageListView.as_view(), name='message-list'),
]
