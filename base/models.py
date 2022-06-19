
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
# from django.contrib.auth.models import User
from django.shortcuts import render


class User(AbstractUser):
    name = models.CharField(max_length=255, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.CharField(max_length=255, null=True, blank=True)
    uuid = models.UUIDField(
        primary_key=False, default=uuid.uuid4, editable=False)

    avator = models.ImageField(
        null=True, blank=True, default='images/avatar.svg')
    # USERNAME_FIELD ='email'
    # REQUIRED_FIELDS = ['username' , 'email' , 'password']


class Topic(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Room(models.Model):
    host = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='host')
    topic = models.ForeignKey(
        Topic, on_delete=models.SET_NULL, null=True, related_name='topic')
    participants = models.ManyToManyField(
        User, related_name='participants', blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def get_online_count(self):
        return self.host.count()

    def join(self, user):
        self.host.add(user)
        self.save()

    def leave(self, user):
        self.host.remove(user)
        self.save()

    def __str__(self) -> str:
        return self.name


class Message(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='message_user')
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE, related_name='message_room')
    body = models.TextField(max_length=255)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['updated', 'created']

    def __str__(self) -> str:
        return self.body[0:50]
