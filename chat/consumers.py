import email
import json
from time import timezone
from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from chat.models import PrivateChatThread, PrivateChatMessage

User = get_user_model()


class PrivateChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_1 = self.scope["user"]
        self.user_2 = self.scope["url_route"]["kwargs"]["userId"]
        self.chat_thread = await sync_to_async(
            PrivateChatThread.objects.get_private_chat_thread
        )(
            self.user_1,
            self.user_2,
        )

        self.other_user_room_group_name = "chat_%s" % self.user_2

        self.room_group_name = "chat_%s" % self.user_1.id

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        sent_by = text_data_json["sent_by"]
        sent_to = text_data_json["sent_to"]
        type = "chat_message"

        self.sender = await sync_to_async(User.get_user.by_email)(email=sent_by)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": type,
                "message": message,
                "sent_by": sent_by,
                "sent_to": sent_to,
                "chat_thread_id": self.chat_thread.id,
            },
        )

        await sync_to_async(PrivateChatMessage.objects.create)(
            chat_thread=self.chat_thread,
            sender=self.sender,
            message_content=message,
            message_type=type,
        )

        await self.channel_layer.group_send(
            self.other_user_room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "sent_by": sent_by,
                "sent_to": sent_to,
                "chat_thread_id": self.chat_thread.id,
            },
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        sent_by = event["sent_by"]
        sent_to = event["sent_to"]
        # Send message to WebSocket
        await self.send(
            text_data=json.dumps(
                {
                    "type": "chat_message",
                    "message": message,
                    "sent_by": sent_by,
                    "sent_to": sent_to,
                    "timestamp": timezone.now().strftime("%b %d,%Y, %H:%M %P"),
                },
                cls=DjangoJSONEncoder,
            )
        )
