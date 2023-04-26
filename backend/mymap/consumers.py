import json
from datetime import datetime, timezone

from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model

from .serializers import MessageSerializer
from .models import Conversation, Message, ConversationUser

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
        type = data['type']
        content = data['content']

        response = None
        if type == 'new_message':
            content['content'] = content['content'].strip()
            if len(content['content']) > 0:
                message = await self.save_message(
                    content['content'],
                    content['user_id'],
                    content['conversation_id'],
                    content['date']
                )
                if message is not None:
                    response = json.dumps({
                        'type': 'new_message',
                        'content': message
                    })
        elif type == 'message_deleted':
            response = json.dumps({
                'type': 'message_deleted',
                'content': content['id']
            })

        if response is not None:
            await self.channel_layer.group_send(self.conversation_group_name, {
                'type': 'conversation.' + type,
                'message': response
            })


    async def conversation_new_message(self, event):
        await self.send(text_data=event['message'])

    async def conversation_message_deleted(self, event):
        await self.send(text_data=event['message'])

    @sync_to_async
    def save_message(self, content, user_id, conversation_id, date):
        try:
            conversation = Conversation.objects.get(pk=conversation_id)
        except Conversation.DoesNotExist:
            print("INTERNAL ERROR: Conversation not found during conversation message saving.")
            return None
        except Conversation.DoesNotExist:
            print("INTERNAL ERROR: Multiple conversation found during conversation message saving.")
            return None

        if not conversation.users.filter(user=user_id).exists():
            print("INTERNAL ERROR: User is not member of this conversation.")
            return None

        notify_with_email = False
        last_message_from_sender = Message.objects.filter(conversation_id=conversation_id, user_id=user_id).order_by("date").last()
        if last_message_from_sender is not None:
            from .mail import delay_instant_notif_conversations

            delta = datetime.now(timezone.utc) - last_message_from_sender.date
            if delta.seconds / 60 >= delay_instant_notif_conversations:
                notify_with_email = True
        else:
            notify_with_email = True

        if notify_with_email:
            from .mail import send_mail_notif_new_message_received

            try:
                sender = User.objects.get(pk=user_id)
            except User.DoesNotExist:
                print("INTERNAL ERROR: Sender not found during conversation message saving.")
                return None
            except User.MultipleObjectsReturned:
                print("INTERNAL ERROR: Multiple sender found during conversation message saving.")
                return None

            receivers = ConversationUser.objects.filter(conversation=conversation).exclude(user=sender)
            for receiver in receivers:
                send_mail_notif_new_message_received(conversation, content, sender, receiver.user)

        message = Message.objects.create(content=content, user_id=user_id, conversation_id=conversation_id, date=date)
        Conversation.objects.filter(pk=conversation_id).update(lastmessagedate=datetime.now(timezone.utc))

        return json.dumps(MessageSerializer(message).data)
