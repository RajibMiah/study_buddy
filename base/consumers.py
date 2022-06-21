import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer

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

    def send_to_socket(self, data):
        self.send(json.dumps(data))

    def to_json_msg(self, msg):
        print("to json msg", msg)
        return{
            'id': '',
            'message_id': '',
            'username': '',
            'body': '',
            'created': '',
            'host': '',
            'avator': '',

        }

    def send_new_msg(self, recv_data):
        data = recv_data['message']
        try:
            if not self.user.is_authenticated:  # new
                return                          # new

            new_msg_obj = Message.objects.create(
                user=self.user, room=self.room, body=data)  # new

            # self.message_data = Message.objects.filter(
            #     room_id=self.room).values().last()

            # print('user id', self.message_data["user_id"])

            # self.user_details = User.objects.filter(
            #     id=self.message_data["user_id"]).values().first()

            # print(json.dumps(
            #     self.user_details, indent=4, sort_keys=True,   cls=DjangoJSONEncoder))

            # self.message_data['type'] = 'chat_message'

            # self.message_data['updated'] = json.dumps(
            #     self.message_data["updated"], indent=4, sort_keys=True,   cls=DjangoJSONEncoder)
            # self.message_data['created'] = json.dumps(
            #     self.message_data["created"], indent=4, sort_keys=True,   cls=DjangoJSONEncoder)

            self.send_to_socket({
                "command": 'NEW_MSG',
                'message': self.to_json_msg(new_msg_obj)
            })
            self.send_room_msg(msg=self.to_json_msg(
                new_msg_obj), type='chat.message')

        except Exception as e:
            print('exception in new_msg' + str(e))

    def send_room_msg(self, msg, type):

        try:
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    "type": type,
                    "message": msg
                },
            )

        except Exception as e:
            print("error while sending"+str(e))

    def chat_message(self, event):
        msg = event["message"]
        self.send_to_socket({
            'command': 'NEW_MSG',
            'message': msg,
        })

    def receive(self, text_data=None, bytes_data=None):
        recv_data = json.loads(text_data)

        if recv_data['command'] == 'MESSAGE':
            pass
        elif recv_data['command'] == 'NEW_MSG':
            self.send_new_msg(recv_data)
        else:
            pass
