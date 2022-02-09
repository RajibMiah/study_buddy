
from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import render

class Topic(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name

class Room(models.Model):
    host = models.ForeignKey(User , on_delete=models.SET_NULL , null= True)
    topic = models.ForeignKey(Topic , on_delete= models.SET_NULL ,null=True)
    # participants = models.ForeignKey()
    name = models.CharField(max_length=255)
    description = models.TextField(null=True , blank=True)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated' , '-created']

    def __str__(self) -> str:
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User , on_delete = models.CASCADE)
    room = models.ForeignKey(Room , on_delete = models.CASCADE)
    body = models.TextField(max_length=255)
    updated = models.DateTimeField(auto_now=True)
    created  = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.body[0:50]

