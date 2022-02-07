import imp
from django.contrib import admin
from .models import Room ,  Message , Topic
# Register your models here.

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    pass

@admin.register(Message)
class Message(admin.ModelAdmin):
    pass

@admin.register(Topic)
class Topic(admin.ModelAdmin):
    pass