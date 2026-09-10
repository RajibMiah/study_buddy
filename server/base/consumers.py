import json

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
