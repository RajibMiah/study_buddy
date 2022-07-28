from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='profile', on_delete=models.CASCADE)
    status = models.CharField(default="Hi i'm using dj chat", max_length=255)
    online = models.BooleanField(default=False)

    def __str__(self):
        return str(self.pk)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.create(user_id=instance.pk)


class Message(models.Model):
    text = models.TextField()
    date_time = models.DateTimeField(auto_now_add=True, blank=True)
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='receiver', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pk)
