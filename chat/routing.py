
from django.urls import path, re_path

from .chatconsumer import ChatConsumer

websocket_urlpatterns = [
    path('ws/chat/<str:reciver_uuid>/',
         ChatConsumer.as_asgi(), name='chat-consumer'),
    # re_path(r'ws/chat/(?P<reciver_uuid>\w+)/$',
    #         ChatConsumer.as_asgi(), name='chat-consumer'),
]
