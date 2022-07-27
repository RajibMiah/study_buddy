
from django.urls import path, re_path

from .chatconsumer import ChatConsumer, VideoChatConsumer

websocket_urlpatterns = [
    path('ws/chat/<str:reciver_uuid>/',
         ChatConsumer.as_asgi(), name='chat-consumer'),
    path('ws/videochat/<str:reciver_uuid>/',
         VideoChatConsumer.as_asgi(), name='vidochat-consumer'),
    # path('ws/videochat/', VideoChatConsumer.as_asgi(), name='videochat-consumer')

]
