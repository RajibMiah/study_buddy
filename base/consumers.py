import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .models import Message, Room


class RoomConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_name = None
        self.room_group_name = None
        self.room = None
        self.user = None  # new

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_name}'
        self.room = Room.objects.get(pk=self.room_name)
        self.user = self.scope['user']  # new
        # connection has to be accepted
        self.accept()

        # join the room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name,
        )

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name,
        )

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        print('text', text_data_json)
        message = text_data_json['message']

        if not self.user.is_authenticated:  # new
            return                          # new

        Message.objects.create(
            user=self.user, room=self.room, body=message)  # new

        self.message_data = Message.objects.filter(
            room_id=self.room).values().last()

        self.message_data['type'] = 'chat_message'
        # self.message_data['updated'] = str(self.message_data.update.utcnow())
        # self.message_data['created'] = str(self.message_data.created.utcnow())

        print(self.message_data)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            # self.message_data
        )
        # Message.objects.create(
        #     user=self.user, room=self.room, body=message)  # new

    def chat_message(self, event):
        print(" prinfing event object", event)
        self.send(text_data=json.dumps(event))
