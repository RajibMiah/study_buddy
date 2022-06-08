import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.core.serializers.json import DjangoJSONEncoder

from .models import Message, Room, User


class RoomConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_name = None
        self.room_group_name = None
        self.room = None
        self.user = None  # new
        self.user_details = None

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
        message = text_data_json['message']

        if not self.user.is_authenticated:  # new
            return                          # new

        Message.objects.create(
            user=self.user, room=self.room, body=message)  # new

        self.message_data = Message.objects.filter(
            room_id=self.room).values().last()

        print('user id', self.message_data["user_id"])

        self.user_details = User.objects.filter(
            id=self.message_data["user_id"]).values().first()

        print(self.user_details)

        # print(json.dumps(
        #     self.user_details, indent=4, sort_keys=True,   cls=DjangoJSONEncoder))

        self.message_data['type'] = 'chat_message'

        self.message_data['updated'] = json.dumps(
            self.message_data["updated"], indent=4, sort_keys=True,   cls=DjangoJSONEncoder)
        self.message_data['created'] = json.dumps(
            self.message_data["created"], indent=4, sort_keys=True,   cls=DjangoJSONEncoder)

        # self.user_obj = dict()
        # for key, value in self.user_details.items:
        #     if json.dumps(self.message_data[key], indent=4, sort_keys=True,   cls=DjangoJSONEncoder):

        #         self.user_obj[key] = value
        #     else:
        #         self.user_obj[key] = json.dumps(
        #             self.message_data[key], indent=4, sort_keys=True,   cls=DjangoJSONEncoder)
        # print(self.user_obj)
        # self.message_data['user'] = self.user_details

        # print(self.message_data)
        # print(type(self.message_data))

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            self.message_data
        )

    def chat_message(self, event):
        # print(" prinfing event object", event)
        self.send(text_data=json.dumps(event))