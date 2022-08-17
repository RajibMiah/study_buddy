
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

# from django.contrib.auth.models import User


class User(AbstractUser):
    GENGER_CHOICE_FIELDS = [
        ('M', 'MALE'),
        ('F', 'FEMALE'),
        ('O', 'OTHER'),
    ]
    name = models.CharField(max_length=255, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.CharField(max_length=255, null=True, blank=True)
    uuid = models.UUIDField(
        primary_key=False, default=uuid.uuid4, editable=False)

    avator = models.ImageField(
        null=True, blank=True, default='/user.png')
    Gender = models.CharField(max_length=20,
                              choices=GENGER_CHOICE_FIELDS, null=True, blank=True)
    location = models.URLField(max_length=200, null=True, blank=True)
    github = models.URLField(max_length=200, null=True, blank=True)
    linkedin = models.URLField(max_length=200, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    summary = models.TextField(null=True, blank=True)

    # USERNAME_FIELD ='email'
    # REQUIRED_FIELDS = ['username' , 'email' , 'password']


class Skill(models.Model):
    user = models.ForeignKey(
        User, related_name='user_skills', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True, null=True)


class WorkExperiance(models.Model):
    user = models.ForeignKey(
        User, related_name='experiances', on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    desgination = models.CharField(max_length=255, blank=True, null=True)
    joining_date = models.DateField(null=True)
    ending_date = models.DateField(null=True)


class Topic(models.Model):
    name = models.CharField(max_length=255, unique=True, null=True)

    @property
    def total_rooms(self):
        total_room = self.room_set.all().count()
        return total_room

    def __str__(self) -> str:
        return str(self.name)


class Room(models.Model):
    host = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    participants = models.ManyToManyField(
        User, related_name='participants', blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    room_image = models.ImageField(
        null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     ordering = ['-updated', '-created']

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
    upvote_boolean = models.BooleanField(default=False)
    downvote_boolean = models.BooleanField(default=False)

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

    @property
    def follower(self):
        print(self.user_id)
        return self.user_id

    def __str__(self):
        return str(f"{self.user_id} follows {self.following_user_id}")
