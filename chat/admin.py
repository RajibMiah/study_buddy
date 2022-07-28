from django.contrib import admin

# Register your models here.
from chat.models import Profile


@admin.register(Profile)
class Profile(admin.ModelAdmin):
    list_display = ('user', 'photo', 'status', 'online')
