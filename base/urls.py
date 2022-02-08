from django.urls import path
from base.views import home , room , createRoom
urlpatterns = [
    path('', home , name = 'home'),
    path('room/<str:pk>/' , room , name = 'room'),
    path('create-room' , createRoom  , name ='create-room' )
]