
from django.contrib import admin

from .models import Message, Room, Topic, User, UserFollowing

# Register your models here.


@admin.register(User)
class UserModel(admin.ModelAdmin):
    pass


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    pass


@admin.register(Message)
class Message(admin.ModelAdmin):
    pass


@admin.register(Topic)
class Topic(admin.ModelAdmin):
    pass


@admin.register(UserFollowing)
class UserFollowing(admin.ModelAdmin):
    pass
