from django.contrib import admin

# Register your models here.
from .models import Message, Profile


@admin.register(Profile)
class Profile(admin.ModelAdmin):
    list_display = ('user', 'status', 'online')


admin.site.register(Message)
