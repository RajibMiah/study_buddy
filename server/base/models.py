
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

# from django.contrib.auth.models import User


class User(AbstractUser):
    name = models.CharField(max_length=255, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.CharField(max_length=255, null=True, blank=True)
    uuid = models.UUIDField(
        primary_key=False, default=uuid.uuid4, editable=False)

    avator = models.ImageField(
        null=True, blank=True, default='/user.png')
    # USERNAME_FIELD ='email'
    # REQUIRED_FIELDS = ['username' , 'email' , 'password']


class Topic(models.Model):
    name = models.CharField(max_length=255)

    @property
    def total_rooms(self):
        total_room = self.room_set.all().count()
        return total_room

    def __str__(self) -> str:
        return self.name


class Room(models.Model):
    host = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    participants = models.ManyToManyField(
        User, related_name='participants', blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    room_image = models.ImageField(
        null=True, blank=True, default='/user.png')
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


class Vote(models.Model):
    user = models.ForeignKey(
        User, related_name='voted_user', on_delete=models.CASCADE)
    room = models.ForeignKey(
        Room, related_name='voted_room', on_delete=models.CASCADE)
    upvote = models.PositiveIntegerField(blank=True,  default=0)
    downvote = models.PositiveIntegerField(blank=True,  default=0)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def total_vote(self):
        return str(self.upvote - self.downvote)

    def __str__(self) -> str:
        return str(f'{self.user.username} voted on {self.room.name} room')


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    voted_message = models.ManyToManyField(
        Vote, related_name='voted_message', blank=True)
    body = models.TextField(max_length=255)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['updated', 'created']

    def __str__(self) -> str:
        return self.body[0:50]


class UserFollowing(models.Model):
    user_id = models.ForeignKey(
        User, related_name='following', on_delete=models.CASCADE)
    following_user_id = models.ForeignKey(
        User, related_name='followers', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user_id', 'following_user_id'], name="unique_followers")
        ]

        ordering = ['-created']

    def __str__(self):
        return str(f"{self.user_id} follows {self.following_user_id}")
