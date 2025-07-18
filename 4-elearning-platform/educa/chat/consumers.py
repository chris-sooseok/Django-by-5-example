import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from django.utils import timezone
from chat.models import Message

class ChatConsumer(AsyncWebsocketConsumer):
    # ChatConsumer is a synchronous consumer, so it needs async_to_sync to handle async action
    async def connect(self):
        self.user = self.scope['user']
        self.id = self.scope['url_route']['kwargs']['course_id']
        self.room_group_name = f'chat_{self.id}'
        # join room group
        # channel_name is an attribute of Consumer
        # await async_to_sync(self.channel_layer.group_add)(
        #     self.room_group_name, self.channel_name
        # )
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )
        await self.accept()
    async def disconnect(self, close_code):
        # leave room group
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    async def persist_message(self, message):
        # send message to WebSocket
        await Message.objects.acreate(
            user=self.user, course_id=self.id, content=message
        )

    # receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        now = timezone.now()
        # # send message to WebSocket
        # self.send(text_data=json.dumps({'message': message}))

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': self.user.username,
                'datetime': now.isoformat(),
            }
        )

        await self.persist_message(message)

    # receive message from room group
    async def chat_message(self, event):
        # send message to WebSocket of each client
        await self.send(text_data=json.dumps(event))