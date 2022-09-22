import json

from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model

from .serializers import MessageSerializer
from .models import Conversation, Message

User = get_user_model()
from asgiref.sync import sync_to_async


class ConversationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.conversation_group_name = 'conversation_%s' % self.conversation_id

        await self.channel_layer.group_add(self.conversation_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.conversation_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        content = data['content']
        conversation_id = data['conversation_id']
        user_id = data['user_id']
        date = data.get('date')

        message = await self.save_message(content, user_id, conversation_id, date)

        await self.channel_layer.group_send(
            self.conversation_group_name,
            {
                'type': 'conversation_message',
                'message': message,
            }
        )

    async def conversation_message(self, event):
        message = event['message']

        await self.send(
            text_data=json.dumps(
                MessageSerializer(message).data
            )
        )

    @sync_to_async
    def save_message(self, content, user_id, conversation_id, date):
        user = User.objects.get(pk=user_id)
        conversation = Conversation.objects.get(pk=conversation_id)
        conversation.up2date_buyer = False
        conversation.up2date_owner = False
        conversation.save()
        return Message.objects.create(
            content=content, user=user, conversation=conversation, date=date
        )
