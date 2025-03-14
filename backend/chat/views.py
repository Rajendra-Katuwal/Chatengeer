from rest_framework import generics, permissions
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from django.contrib.auth import get_user_model


User = get_user_model()

class ConversationCreateView(generics.CreateAPIView):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """Automatically add the request user to the conversation"""
        conversation = serializer.save()
        conversation.participants.add(self.request.user)  # Add the logged-in user

class MessageCreateView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """Automatically set the sender to the logged-in user"""
        serializer.save(sender=self.request.user)

class MessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Return messages only for the requested conversation"""
        conversation_id = self.kwargs['conversation_id']
        return Message.objects.filter(conversation__id=conversation_id)
