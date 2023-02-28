import json
from datetime import datetime, timezone

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

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.conversation_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)

        message = await self.save_message(data['content'], data['user_id'], data['conversation_id'], data['date'])

        await self.channel_layer.group_send(
            self.conversation_group_name,
            {
                'type': 'conversation.message',
                'message': message,
            }
        )

    async def conversation_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps(MessageSerializer(message).data))

    @sync_to_async
    def save_message(self, content, user_id, conversation_id, date):
        notify_with_email = False
        last_message_from_sender = Message.objects.filter(conversation_id=conversation_id, user_id=user_id).last()
        if last_message_from_sender is not None:
            from .mail import delay_instant_notif_conversations

            delta = datetime.now(timezone.utc) - last_message_from_sender.date
            if delta.seconds / 60 >= delay_instant_notif_conversations:
                notify_with_email = True
        else:
            notify_with_email = True

        if notify_with_email:
            from .mail import send_mail_notif_new_message_received

            conversation = Conversation.objects.get(pk=conversation_id)
            if conversation.buyer_id == user_id:
                receiver = conversation.owner
            else:
                receiver = conversation.buyer
            send_mail_notif_new_message_received(conversation, content, receiver)

        message = Message.objects.create(content=content, user_id=user_id, conversation_id=conversation_id, date=date)
        Conversation.objects.filter(pk=conversation_id).update(lastmessagedate=datetime.now(timezone.utc))

        return message
