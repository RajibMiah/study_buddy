from django.contrib import admin

from .models import Message, Notification, contact

# Register your models here.
# admin.site.register(User)
admin.site.register(Message)
admin.site.register(contact)
admin.site.register(Notification)
