from django.urls import path

from chat.consumers.message import MessageConsumer
from chat.consumers.notification import NewUserConsumer

websocket_urlpatterns = [
    path('ws/notification/', NewUserConsumer.as_asgi()),
    path('ws/message/<str:username>/', MessageConsumer.as_asgi())
]
