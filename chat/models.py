
from django.conf import settings
from django.db import models
from pyexpat import model


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


class Notification(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='sender_details', on_delete=models.CASCADE)
    notification_body = models.CharField(max_length=255)
    is_seen = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)
