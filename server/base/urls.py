
from django.urls import include, path

from base.views import *

urlpatterns = [

    path('login/', login, name='login-user'),
    path('logout/', logout, name='logout'),
    path('register/', registerPage, name='register-user'),
    path('delete-message/<str:pk>', deleteMessage, name='delete-message'),

    path('', home, name='home'),
    path('profile/<str:pk>/', userProfile, name='user-profile'),
    path('room/<str:pk>/', room, name='room'),
    path('create-room/', createRoom, name='create-room'),
    path('update-room/<str:pk>/', updateRoom, name='update-room'),
    path('delete-room/<str:pk>/', deleteRoom, name='delete-room'),

    path('update-user/', updateUser, name="update-user"),

    path('topics/', topicsPage, name="topics"),
    path('activity/', activityPage, name="activity"),

    path('api/', include('base.api.urls'))

]
