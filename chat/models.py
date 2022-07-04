
import random
from datetime import datetime

from django.conf import Settings, settings
from django.db import models


class Message(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='sender', on_delete=models.CASCADE)
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='recipient', on_delete=models.CASCADE)
    is_readed = models.BooleanField(default=False)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.username

    def recent_msgs(self):
        return Message.objects.order_by('timestamp').all()


class contact(models.Model):
    channel_name = models.TextField(null=True)
    contact_id = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='contact', on_delete=models.DO_NOTHING)

    def __str__(self):
        return str(self.contact_id)


# VIDEO  CHAT MODEL

def UniqueGenerator(length=10):
    source = "abcdefghijklmnopqrztuvwxyz"
    result = ""
    for _ in range(length):
        result += source[random.randint(0, length)]
    return result

# Create your models here.


class GroupChat(models.Model):
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    unique_code = models.CharField(max_length=10, default=UniqueGenerator)
    date_created = models.DateTimeField(default=datetime.now)

# THREAD STATUS


status_list = {
    0: 'Contacting',
    1: 'Not available',
    2: 'Accepted',
    3: 'Rejected',
    4: 'Busy',
    5: 'Processing',
    6: 'Ended',
}


class VideoThread(models.Model):
    caller = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='caller_user')
    callee = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='calle_user')
    status = models.IntegerField(default=0)
    date_started = models.DateTimeField(default=datetime.now)
    date_ended = models.DateTimeField(default=datetime.now)
    date_created = models.DateTimeField(default=datetime.now)

    @property
    def status_name(self):
        return status_list[self.status]

    @property
    def duration(self):
        return self.date_ended - self.date_started


class Notification(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='sender_details', on_delete=models.CASCADE)
    notification_body = models.CharField(max_length=255)
    is_seen = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)
