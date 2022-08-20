import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.db.models import Q

from .models import Message, Room, User


class RoomConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_id = None
        self.room_group_name = None
        self.room = None
        self.user = None  # new
        self.user_details = None

    def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'
        self.room = Room.objects.get(pk=self.room_id)
        # self.user_details = User.objects.get(id=self.room_id)
        self.user = self.scope['user']  # new

        # connection has to be accepted
        self.accept()
        print('Room connected')
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

        try:
            user = User.objects.get(
                Q(username=self.user) and Q(uuid=self.user.uuid))
            msg_set = user.message_set.all()[:1]

        except Exception as e:
            print('exception in new_msg ' + str(e))

        return{
            'id': user.id,
            'message_id': str(msg_set[0].id),
            'username': str(user.name),
            'body': str(msg),
            'created': str(msg_set[0].created),
            'avator': str(user.avator.url),

        }

    def send_new_msg(self, recv_data):
        data = recv_data['message']
        self.send_room_msg(msg=recv_data, type='chat.message')
        # try:

        #     new_msg_obj = Message.objects.create(
        #         user=data.userId, room=self.room, body=data)  # new

        #     # self.send_to_socket({
        #     #     "command": 'NEW_MSG',
        #     #     'message': self.to_json_msg(new_msg_obj)
        #     # })
        #     room = Room.objects.get(id=self.room_id)
        #     if not room.participants.filter(id=data.userId).exists():
        #         room.participants.add(self.user)
        #         user = User.objects.get(
        #             Q(username=data.userName) and Q(id=data.userId))

        #         ctx = {
        #             'id': user.id,
        #             'username': str(user.userName),
        #             'avator': str(user.avator.url),
        #         }

        #         self.send_to_socket({
        #             'command': 'PARTICIPANTS_ADDED',
        #             'message': ctx
        #         })
        #         self.send_room_msg(msg=ctx, type='chat.message')
        #     else:
        #         print('user exit')

        #     self.send_room_msg(msg=self.to_json_msg(
        #         new_msg_obj), type='chat.message')

        # except Exception as e:
        #     print('exception in new_msg' + str(e))

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
        print("recived data", recv_data)

        if recv_data['command'] == 'MESSAGE':
            pass
        elif recv_data['command'] == 'NEW_MSG':
            self.send_new_msg(recv_data)
        else:
            pass
