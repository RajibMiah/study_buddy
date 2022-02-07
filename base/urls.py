from django.urls import path
from base.views import home , room
urlpatterns = [
    path('', home , name = 'name'),
    path('room/<str:pk>/' , room , name = 'room')
]