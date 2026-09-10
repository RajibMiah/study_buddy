from django.urls import re_path

from .consumers import CallConsumer, RoomConsumer

websocket_urlpatterns = [
    re_path(r"ws/room/(?P<room_id>\w+)/$", RoomConsumer.as_asgi(), name="ws-room"),
    re_path(r"ws/call/(?P<room_id>\w+)/$", CallConsumer.as_asgi(), name="ws-call"),
]
