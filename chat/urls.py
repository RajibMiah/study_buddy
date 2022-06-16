
from django.urls import path

from . import views

urlpatterns = [
    path('', views.chatpage, name='chat'),
    path('<str:reciver_uuid>/', views.targeted_recipient, name='message-chat'),

]
