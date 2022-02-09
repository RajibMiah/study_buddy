
from django.urls import path
from base.views import *
urlpatterns = [

    path('login/', login , name = 'login'),
    path('logout/' , logout , name = 'logout'),
    path('register/', registerPage , name = 'register-user'),

    path('', home , name = 'home'),
    path('room/<str:pk>/' , room , name = 'room'),
    path('create-room/' , createRoom  , name ='create-room' ),
    path('update-room/<str:pk>/' , updateRoom , name = 'update-room'),
    path('delete-room/<str:pk>/' , deleteRoom , name = 'delete-room' ),
 
]