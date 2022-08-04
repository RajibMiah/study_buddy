
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from base.views import *

from .api.views import GetRooms, UserProfile

router = DefaultRouter()
router.register('rooms', GetRooms, basename='room-details')
router.register('profile', UserProfile, basename='user-profile')

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

    path('api/v1/', include(router.urls)),
    path('api/', include('api.urls'))
]
