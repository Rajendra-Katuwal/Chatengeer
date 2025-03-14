import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message, Conversation
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversation_id = self.scope["url_route"]["kwargs"]["conversation_id"]
        self.room_group_name = f"chat_{self.conversation_id}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        user = self.scope["user"]

        if user.is_authenticated:
            message = await self.save_message(user, data["message"])
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message.text,
                    "sender": user.username,
                },
            )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    async def save_message(self, user, message_text):
        conversation = await Conversation.objects.aget(id=self.conversation_id)
        return await Message.objects.acreate(conversation=conversation, sender=user, text=message_text)
