
import json
import os
import threading
import time
import uuid
from datetime import datetime

import django
from asgiref.sync import async_to_sync, sync_to_async
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from channels.exceptions import StopConsumer
from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.query_utils import Q

from .models import Message, Notification, VideoThread, contact

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

User = get_user_model()


class ChatConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_name = None
        self.room_group_name = None
        self.room = None
        self.user = None  # new
        self.user_details = None
        self.recciver_uuid = None

    def connect(self):
        print('------------connected------------')
        self.recciver_uuid = self.scope['url_route']['kwargs']['reciver_uuid']
        self.user = User.objects.get(username=self.scope['user'])
        contact.objects.filter(contact_id=self.user).delete()
        contact.objects.create(
            channel_name=self.channel_name, contact_id=self.user)
        self.accept()
        self.PING_ACK = True
        pinger = threading.Thread(target=self.ping)

        pinger.start()

    def send_to_socket(self, data):
        self.send(json.dumps(data))

    def get_all_cache_chat(self):
        try:
            msgs = Message.objects.values('sender', 'recipient').filter(
                Q(recipient=self.user) | Q(sender=self.user)).order_by('timestamp')
            self.user_list = list()
            msg_list = list()
            for msg in msgs:
                sid = msg['sender']
                if sid == self.user.id:
                    sid = msg['recipient']

                if sid not in self.user_list:
                    self.user_list.append(sid)
                    msg_list.append(self.chat_load(data={'user': sid}))

            self.send_to_socket({
                'command': 'LOAD_MSGS',
                'msg_list': msg_list,
            })

        except Exception as e:
            print("exception in cahcing chat" + str(e))
            pass

    def get_cache_chat(self, data):
        print('from get_cach_data', data)
        try:
            msgs = Message.objects.values('sender', 'recipient').filter(
                Q(recipient=self.user) | Q(sender=self.user)).order_by('timestamp')
            self.user_list = list()
            msg_list = list()
            for msg in msgs:
                sid = msg['sender']
                if sid == self.user.id:
                    sid = msg['recipient']

                if sid not in self.user_list:
                    self.user_list.append(sid)
                    msg_list.append(self.chat_load(data={'user': sid}))

            self.send_to_socket({
                'command': 'LOAD_MSGS',
                'msg_list': msg_list,
            })

        except Exception as e:
            print("exception in cahcing chat" + str(e))
            pass

    def check_user_load(self, data):

        # NOTE:: NOT USER DATA OR USER
        print('check user load data', data)
        recipient = User.objects.get(uuid=self.reciver_uuid)
        msg_set = Message.objects.filter((Q(sender=self.user) & Q(recipient=recipient)) | (
            Q(sender=self.user) & Q(recipient=recipient))).order_by('-timestamp').all()
        chname = self.get_channel_name(recipient=recipient)
        status = ''
        if chname is None:
            status = "offline"
        else:
            status = "online"
            self.send_chat_msg(
                msg=self.user.id, type="status.ON", reciever=recipient)

        ctx = {
            'recipient_uuid': str(recipient.uuid),
            'contact': data['user'],
            'name': recipient.username,
            'messages': self.to_json_msgs(msg_set),
            'status': status,
            'pic': recipient.avator.url
        }
        return ctx

    def chat_load(self, data):

        recipient = User.objects.get(id=data['user'])
        msg_set = Message.objects.filter((Q(sender=self.user) & Q(recipient=recipient)) | (
            Q(sender=recipient) & Q(recipient=self.user))).order_by('-timestamp').all()
        chname = self.get_channel_name(recipient=recipient)

        status = ''
        if chname is None:
            status = "offline"
        else:
            status = "online"
            self.send_chat_msg(
                msg=self.user.id, type="status.ON", reciever=recipient)

        ctx = {
            'recipient_uuid': str(recipient.uuid),
            'contact': data['user'],
            'name': recipient.username,
            'messages': self.to_json_msgs(msg_set),
            'status': status,
            'pic': recipient.avator.url
        }
        return ctx

    def disconnect(self, code):

        contact.objects.filter(channel_name=self.channel_name).delete()
        try:
            contact.objects.get(contact_id=self.user)
        except contact.DoesNotExist as e:
            for item in self.user_list:
                rec = User.objects.get(pk=item)
                self.send_chat_msg(
                    msg=self.user.id, type="status.OFF", reciever=rec)
        raise StopConsumer()

    # this recieves msg from other channel and sends to the current user

    def chat_message(self, event):
        msg = event["message"]
        self.send_to_socket({
            'command': 'NEW_MSG',
            'message': msg,
            'user_uuid': str(self.user.uuid),

        })
        if(msg["sid"] not in self.user_list and msg['sid'] != self.user.id):
            self.user_list.append(msg["sid"])
            rec = User.objects.get(pk=msg["sid"])
            self.send_chat_msg(
                msg=self.user.id, type="status.ON", reciever=rec)

    def ping(self):
        while True:
            time.sleep(4)
            if self.PING_ACK == True:
                self.PING_ACK = False
                self.send_to_socket({'command': 'PING'})
            else:
                self.disconnect(code=1001)

    def pong(self, event):
        self.PING_ACK = True

    def status_OFF(self, event):
        id = event["message"]
        if id in self.user_list:
            self.user_list.remove(id)
            self.send_to_socket({
                "command": "OFFLINE",
                "message": id
            })

    def status_ON(self, event):
        id = event["message"]
        if id not in self.user_list:
            self.user_list.append(id)
        self.send_to_socket({
            "command": "ONLINE",
            "message": id
        })

    def new_msg(self, recv_data):
        data = recv_data["message"]
        try:
            sender_user = User.objects.filter(username=data['sender'])[0]
            recipient_user = User.objects.filter(username=data['recipient'])[0]
            msg = Message.objects.create(
                sender=sender_user,
                recipient=recipient_user,
                content=data["content"],
            )
            notify = Notification.objects.create(
                user=recipient_user, notification_body=data["content"], is_seen=False)

            # send group socket for upcomming new message
            self.send_to_socket({
                "command": "NEW_MSG",
                "message": self.to_json_msg(msg),
                "reciver_uuid": str(recipient_user.uuid)
            })

            # send notificition message socket
            self.send_to_socket({
                "command": "NOTIFY",
                "message": {
                    "user_id": str(notify.user.id),
                    "notification_body": str(notify.notification_body),
                    "is_seen": notify.is_seen,
                }
            })
            self.send_chat_msg(msg=self.to_json_msg(
                msg), type="chat.message", reciever=recipient_user)

        except Exception as e:
            print("exception in new_msg()" + str(e))

    def get_channel_name(self, recipient):
        try:
            chanel = contact.objects.get(contact_id=recipient)
            return chanel.channel_name
        except contact.DoesNotExist:
            return None

    # for sending msg to another channel(to recipient's channel)
    def send_chat_msg(self, msg, type, reciever):
        try:
            ch_name = self.get_channel_name(recipient=reciever)
            if ch_name is not None:
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.send)(ch_name, {
                    "type": type,
                    "message": msg
                })
        except Exception as e:
            print("error while sending"+str(e))

    def search_result(self, data):

        try:
            result_set = User.objects.values('id', 'username', 'avator', 'uuid').filter(
                username__contains=data["text"]).exclude(id=self.user.id)[:10]
            contact_list = list()

            for item in result_set:
                # if not item['username'] == self.user.username:
                contact_list.append({
                    "id": item["id"],
                    "name": item['username'],
                    "uname": item['username'],
                    "pic": settings.MEDIA_URL+item['avator'],
                    "recipient_uuid": str(item['uuid'])
                })
            print(contact_list)
            self.send_to_socket({
                "command": "SEARCH",
                "result": contact_list
            })
        except Exception as e:
            print(e)

    def add_new_contact(self, data):
        contact = User.objects.get(pk=data['id'])
        if data['id'] not in self.user_list:
            self.user_list.append(data['id'])

        chname = self.get_channel_name(recipient=data['id'])
        status = ''
        if chname is None:
            status = "offline"
        else:
            status = "online"
        self.send_to_socket({
            "command": "NEW_CONT",
            "id": contact.id,
            "name": contact.username,
            "pic": contact.avator.url,
            "status": status,
            "recipient_uuid": str(contact.uuid)
        })

    def chat_MAR(self, event):
        self.send_to_socket({
            "command": "MAR",
            "message": event["message"]
        })

    # if user reads the messages of sender
    def mark_as_read(self, data):
        sen = User.objects.get(pk=data["message"])
        un_read_msgs = Message.objects.values("id").filter(
            sender=sen, recipient=self.user, is_readed=False)
        for unread in un_read_msgs:
            msg = Message.objects.get(pk=unread["id"])
            msg.is_readed = True
            msg.save()
        self.send_chat_msg(msg=self.user.id, type="chat.MAR", reciever=sen)

    def to_json_msgs(self, msgs):
        msg_list = []
        for msg in msgs:
            msg_list.append(self.to_json_msg(msg))
        return msg_list

    def to_json_msg(self, msg):

        return{
            'sid': msg.sender.id,
            'rid': msg.recipient.id,
            'sender': msg.sender.username,
            'recipient': msg.recipient.username,
            'content': msg.content,
            'time_stamp': str(msg.timestamp).split('.')[0],
            'is_readed': msg.is_readed,
            'pic': msg.sender.avator.url
        }

    # this recieves from socket

    def receive(self, text_data):
        recv_data = json.loads(text_data)
        # print(recv_data)

        if recv_data['command'] == 'PONG':
            self.pong(recv_data)
        elif recv_data['command'] == 'NEW_MSG':
            self.new_msg(recv_data)
        elif recv_data['command'] == 'GET_ALL_CACHE_CHAT':
            self.get_all_cache_chat()
        elif recv_data['command'] == 'SEARCH':
            self.search_result(recv_data)
        elif recv_data['command'] == 'NEW_CONTACT':
            self.add_new_contact(recv_data)
        elif recv_data['command'] == 'MAR':
            self.mark_as_read(recv_data)
        elif recv_data['command'] == 'CHECK_RECIPIENT_MSG':
            self.check_user_load(recv_data)
        else:
            pass


# Video Call Status
VC_CONTACTING, VC_NOT_AVAILABLE, VC_ACCEPTED, VC_REJECTED, VC_BUSY, VC_PROCESSING, VC_ENDED, VC_DROP = \
    0, 1, 2, 3, 4, 5, 6, 7


class VideoChatConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        self.user = self.scope['user']
        self._uuid = self.scope['url_route']['kwargs']['reciver_uuid']
        self.user_room_id = f"videochat_{self.user.id}"
        print('=================== print uuid =========================')
        print("video chat uuid", self._uuid)
        print('=================== end print uuid =====================')
        await self.channel_layer.group_add(
            self.user_room_id,
            self.channel_name
        )

        await self.send({
            'type': 'websocket.accept'
        })

    async def websocket_disconnect(self, event):
        video_thread_id = self.scope['session'].get('video_thread_id', None)
        videothread = await self.change_videothread_status(video_thread_id, VC_ENDED)
        if videothread is not None:
            await self.change_videothread_datetime(video_thread_id, False)
            await self.channel_layer.group_send(
                f"videochat_{videothread.caller.id}",
                {
                    'type': 'chat_message',
                    'message': json.dumps({'type': "offerResult", 'status': VC_ENDED, 'video_thread_id': videothread.id}),
                }
            )
            await self.channel_layer.group_send(
                f"videochat_{videothread.callee.id}",
                {
                    'type': 'chat_message',
                    'message': json.dumps({'type': "offerResult", 'status': VC_ENDED, 'video_thread_id': videothread.id}),
                }
            )
        await self.channel_layer.group_discard(
            self.user_room_id,
            self.channel_name
        )
        raise StopConsumer()

    async def websocket_receive(self, event):
        text_data = event.get('text', None)
        bytes_data = event.get('bytes', None)

        if text_data:
            text_data_json = json.loads(text_data)
            message_type = text_data_json['type']
            # print('=================== print message_type =========================')
            # print("video chat uuid", message_type)
            # print('=================== end print message_type =====================')
            print()
            if message_type == "createOffer":
                callee_uuid = text_data_json['uuid']
                status, video_thread_id = await self.create_videothread(callee_uuid)

                await self.send({
                    'type': 'websocket.send',
                    'text': json.dumps({'type': "offerResult", 'status': status, 'video_thread_id': video_thread_id})
                })

                if status == VC_CONTACTING:
                    videothread = await self.get_videothread(video_thread_id)

                    await self.channel_layer.group_send(
                        f"videochat_{videothread.callee.id}",
                        {
                            'type': 'chat_message',
                            'message': json.dumps({'type': "offer", 'username': self.user.username, 'video_thread_id': video_thread_id}),
                        }
                    )

            elif message_type == "cancelOffer":
                video_thread_id = text_data_json['video_thread_id']
                videothread = await self.get_videothread(video_thread_id)
                self.scope['session']['video_thread_id'] = None
                self.scope['session'].save()

                if videothread.status != VC_ACCEPTED or videothread.status != VC_REJECTED:
                    await self.change_videothread_status(video_thread_id, VC_NOT_AVAILABLE)
                    await self.send({
                        'type': 'websocket.send',
                        'text': json.dumps({'type': "offerResult", 'status': VC_NOT_AVAILABLE, 'video_thread_id': videothread.id})
                    })
                    await self.channel_layer.group_send(
                        f"videochat_{videothread.callee.id}",
                        {
                            'type': 'chat_message',
                            'message': json.dumps({'type': "offerFinished"}),
                        }
                    )
            elif message_type == "dropOffer":
                video_thread_id = text_data_json['video_thread_id']
                videothread = await self.get_videothread(video_thread_id)
                self.scope['session']['video_thread_id'] = None
                self.scope['session'].save()

                if videothread.status != VC_ACCEPTED or videothread.status != VC_REJECTED:
                    await self.change_videothread_status(video_thread_id, VC_DROP)
                    await self.send({
                        'type': 'websocket.send',
                        'text': json.dumps({'type': "offerResult", 'status': VC_DROP, 'video_thread_id': videothread.id})
                    })
                    await self.channel_layer.group_send(
                        f"videochat_{videothread.callee.id}",
                        {
                            'type': 'chat_message',
                            'message': json.dumps({'type': "offerFinished"}),
                        }
                    )
                print('Offer has been droped')
            elif message_type == "acceptOffer":
                video_thread_id = text_data_json['video_thread_id']
                videothread = await self.change_videothread_status(video_thread_id, VC_PROCESSING)
                await self.change_videothread_datetime(video_thread_id, True)

                await self.channel_layer.group_send(
                    f"videochat_{videothread.caller.id}",
                    {
                        'type': 'chat_message',
                        'message': json.dumps({'type': "offerResult", 'status': VC_ACCEPTED, 'video_thread_id': videothread.id}),
                    }
                )

            elif message_type == "rejectOffer":
                video_thread_id = text_data_json['video_thread_id']
                videothread = await self.change_videothread_status(video_thread_id, VC_REJECTED)
                self.scope['session']['video_thread_id'] = None
                self.scope['session'].save()

                await self.channel_layer.group_send(
                    f"videochat_{videothread.caller.id}",
                    {
                        'type': 'chat_message',
                        'message': json.dumps({'type': "offerResult", 'status': VC_REJECTED, 'video_thread_id': videothread.id}),
                    }
                )

            elif message_type == "hangUp":
                video_thread_id = text_data_json['video_thread_id']
                videothread = await self.change_videothread_status(video_thread_id, VC_ENDED)
                await self.change_videothread_datetime(video_thread_id, False)
                self.scope['session']['video_thread_id'] = None
                self.scope['session'].save()

                await self.channel_layer.group_send(
                    f"videochat_{videothread.caller.id}",
                    {
                        'type': 'chat_message',
                        'message': json.dumps({'type': "offerResult", 'status': VC_ENDED, 'video_thread_id': videothread.id}),
                    }
                )
                await self.channel_layer.group_send(
                    f"videochat_{videothread.callee.id}",
                    {
                        'type': 'chat_message',
                        'message': json.dumps({'type': "offerResult", 'status': VC_ENDED, 'video_thread_id': videothread.id}),
                    }
                )

            elif message_type == "callerData":
                video_thread_id = text_data_json['video_thread_id']
                videothread = await self.get_videothread(video_thread_id)

                await self.channel_layer.group_send(
                    f"videochat_{videothread.callee.id}",
                    {
                        'type': 'chat_message',
                        'message': text_data,
                    }
                )

            elif message_type == "calleeData":
                video_thread_id = text_data_json['video_thread_id']
                videothread = await self.get_videothread(video_thread_id)

                await self.channel_layer.group_send(
                    f"videochat_{videothread.caller.id}",
                    {
                        'type': 'chat_message',
                        'message': text_data,
                    }
                )

    async def chat_message(self, event):
        message = event['message']

        await self.send({
            'type': 'websocket.send',
            'text': message
        })

    @database_sync_to_async
    def get_videothread(self, id):
        try:
            videothread = VideoThread.objects.get(id=id)
            return videothread
        except VideoThread.DoesNotExist:
            return None

    @database_sync_to_async
    def create_videothread(self, callee_uuid):
        try:
            callee = User.objects.get(uuid=callee_uuid)
        except User.DoesNotExist:
            return 404, None

        if VideoThread.objects.filter(Q(caller_id=callee.id) | Q(callee_id=callee.id), status=VC_PROCESSING).count() > 0:
            return VC_BUSY, None

        videothread = VideoThread.objects.create(
            caller_id=self.user.id, callee_id=callee.id)
        self.scope['session']['video_thread_id'] = videothread.id
        self.scope['session'].save()

        return VC_CONTACTING, videothread.id

    @database_sync_to_async
    def change_videothread_status(self, id, status):
        try:
            videothread = VideoThread.objects.get(id=id)
            videothread.status = status
            videothread.save()
            return videothread
        except VideoThread.DoesNotExist:
            return None

    @database_sync_to_async
    def change_videothread_datetime(self, id, is_start):
        try:
            videothread = VideoThread.objects.get(id=id)
            if is_start:
                videothread.date_started = datetime.now()
            else:
                videothread.date_ended = datetime.now()
            videothread.save()
            return videothread
        except VideoThread.DoesNotExist:
            return None
