import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Conversation, Message
from django.contrib.auth import get_user_model
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

        await self.save_message(content, user_id, conversation_id)

        await self.channel_layer.group_send(
            self.conversation_group_name,
            {
                'type': 'conversation_message',
                'content': content,
                'conversation_id': conversation_id,
                'user_id': user_id,
            }
        )

    async def conversation_message(self, event):
        content = event['content']
        conversation_id = event['conversation_id']
        user_id = event['user_id']

        await self.send(text_data=json.dumps({
            'content': content,
            'conversation': conversation_id,
            'user_id': user_id
        }))
    
    @sync_to_async
    def save_message(self, content, user_id, conversation_id):
        user = User.objects.get(pk=user_id)
        conversation = Conversation.objects.get(pk=conversation_id)
        conversation.up2date_buyer = False
        conversation.up2date_owner = False
        conversation.save()
        Message.objects.create(content=content, user=user, conversation=conversation)