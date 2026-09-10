import json
import uuid

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.template.defaultfilters import timesince

from .models import Message, Room


class RoomConsumer(WebsocketConsumer):
    """Realtime chat for a single study room.

    Clients send ``{"command": "NEW_MESSAGE", "body": "..."}``. The consumer
    persists the message, adds the sender to the room participants and
    broadcasts the rendered payload to everyone in the room group.
    """

    def connect(self):
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_name = f"room_{self.room_id}"
        self.user = self.scope["user"]

        if not self.user.is_authenticated:
            self.close(code=4401)
            return

        if not Room.objects.filter(pk=self.room_id).exists():
            self.close(code=4404)
            return

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        if getattr(self, "room_group_name", None):
            async_to_sync(self.channel_layer.group_discard)(
                self.room_group_name, self.channel_name
            )

    def receive(self, text_data=None, bytes_data=None):
        try:
            payload = json.loads(text_data or "{}")
        except json.JSONDecodeError:
            return

        if payload.get("command") != "NEW_MESSAGE":
            return

        body = (payload.get("body") or "").strip()
        if not body:
            return

        message = self._persist(body)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {"type": "chat.message", "message": self._serialize(message)},
        )

    def _persist(self, body):
        room = Room.objects.get(pk=self.room_id)
        room.participants.add(self.user)
        return Message.objects.create(user=self.user, room=room, body=body[:255])

    def _serialize(self, message):
        avatar = message.user.avator
        return {
            "id": message.id,
            "user_id": message.user_id,
            "username": message.user.username,
            "name": message.user.name or message.user.username,
            "avatar": avatar.url if avatar else "",
            "body": message.body,
            "created": f"{timesince(message.created)} ago",
        }

    def chat_message(self, event):
        self.send(text_data=json.dumps(event["message"]))


class CallConsumer(WebsocketConsumer):
    """WebRTC signalling relay for a room's video call.

    Peers exchange SDP offers/answers and ICE candidates through this
    consumer; media itself stays peer-to-peer. Messages in:
    ``{"type": "join"}`` announces the peer, ``{"type": "signal",
    "target": <peer_id>, "data": {...}}`` relays to one peer, and
    ``{"type": "leave"}`` tears the peer down.
    """

    def connect(self):
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.user = self.scope["user"]

        if not self.user.is_authenticated:
            self.close(code=4401)
            return
        if not Room.objects.filter(pk=self.room_id).exists():
            self.close(code=4404)
            return

        self.peer_id = uuid.uuid4().hex
        self.room_group = f"call_{self.room_id}"
        self.peer_group = f"callpeer_{self.peer_id}"

        async_to_sync(self.channel_layer.group_add)(self.room_group, self.channel_name)
        async_to_sync(self.channel_layer.group_add)(self.peer_group, self.channel_name)
        self.accept()
        self.send(text_data=json.dumps({"type": "welcome", "peer_id": self.peer_id}))

    def disconnect(self, close_code):
        if getattr(self, "peer_id", None):
            async_to_sync(self.channel_layer.group_send)(
                self.room_group,
                {"type": "call.event", "sender": self.peer_id,
                 "event": {"type": "peer-leave", "peer_id": self.peer_id}},
            )
        for group in (getattr(self, "room_group", None), getattr(self, "peer_group", None)):
            if group:
                async_to_sync(self.channel_layer.group_discard)(group, self.channel_name)

    def receive(self, text_data=None, bytes_data=None):
        try:
            msg = json.loads(text_data or "{}")
        except json.JSONDecodeError:
            return

        kind = msg.get("type")
        identity = {
            "peer_id": self.peer_id,
            "username": self.user.username,
            "name": self.user.name or self.user.username,
        }

        if kind == "join":
            async_to_sync(self.channel_layer.group_send)(
                self.room_group,
                {"type": "call.event", "sender": self.peer_id,
                 "event": {"type": "peer-join", **identity}},
            )
        elif kind == "signal" and msg.get("target"):
            async_to_sync(self.channel_layer.group_send)(
                f"callpeer_{msg['target']}",
                {"type": "call.event", "sender": self.peer_id,
                 "event": {"type": "signal", "data": msg.get("data"), **identity}},
            )
        elif kind == "leave":
            async_to_sync(self.channel_layer.group_send)(
                self.room_group,
                {"type": "call.event", "sender": self.peer_id,
                 "event": {"type": "peer-leave", "peer_id": self.peer_id}},
            )

    def call_event(self, event):
        if event.get("sender") == self.peer_id:
            return
        self.send(text_data=json.dumps(event["event"]))
