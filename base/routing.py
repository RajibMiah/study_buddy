
from django.urls import path

from .consumers import RoomConsumer

websocket_urlpatterns = [
   
    path('ws/room/', RoomConsumer.as_asgi() , name='room'),
    
]
