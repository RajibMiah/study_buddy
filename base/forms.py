
from dataclasses import fields

from django.contrib.auth import get_user_model
from django.forms import ModelForm

from .models import Room

User = get_user_model()


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username',  'email']


class UserRegisterFrom(ModelForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password']
