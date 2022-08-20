import datetime

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from rest_framework import serializers

from chat.models import Message

User = get_user_model()


AVATOR_BASE_URL = 'http://127.0.0.1:8000/images/'


class MessageSerializer(serializers.Serializer):
    text = serializers.CharField()
    read = serializers.BooleanField(read_only=True)
    date_time = serializers.DateTimeField(required=False)
    sender_id = serializers.IntegerField(read_only=True)
    receiver = serializers.SlugField(write_only=True)

    def create(self, validated_data):

        try:

            user = User.objects.get(username=validated_data['receiver'])

            message = Message()
            message.text = validated_data['text']
            message.sender = self.context['request'].user
            message.receiver = user
            message.save()
            self.__broadcast(message)
            return validated_data
        except Exception as e:

            raise Exception('Error', e)

    def __broadcast(self, message: Message):
        serializer = MessageModelSerializer(message, many=False)
        n_message = serializer.data
        n_message['read'] = False

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'chat_%s' % message.receiver.username, {
                'type': 'new_message',
                'message': n_message
            }
        )


class MessageModelSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(read_only=True, source='sender.username')
    read = serializers.BooleanField(default=True)

    class Meta:
        model = Message
        fields = ('text', 'sender', 'date_time', 'read')


class UsersWithMessageSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    online = serializers.BooleanField(source='profile.online')
    status = serializers.CharField(source='profile.status')
    messages = serializers.SerializerMethodField()


    class Meta:
        model = User
        fields = ('name', 'uuid','username',  'online',
                  'status', 'messages', 'avator')

    def get_name(self, obj):
        if obj.first_name:
            return obj.get_full_name()
        return obj.username

    def get_messages(self, obj):
        messages = Message.objects.filter(
            Q(receiver=obj, sender=self.context['request'].user) |
            Q(sender=obj, receiver=self.context['request'].user)).prefetch_related('sender', 'receiver')
        serializer = MessageModelSerializer(
            messages.order_by('date_time'), many=True)
        return serializer.data


class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    online = serializers.BooleanField(source='profile.online')
    status = serializers.CharField(source='profile.status')
    messages = serializers.SerializerMethodField()
    avator = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'name', 'username', 'online',
                  'status', 'messages', 'avator', 'uuid')

    def get_name(self, obj):
        if obj.first_name:
            return obj.get_full_name()
        return obj.username

    def get_messages(self, obj):
        return []

    def get_avator(self, user):
        if user.avator:
            avator_url = str(AVATOR_BASE_URL) + str(user.avator)
            return avator_url
        return None


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "password", "first_name", "last_name", "email")
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        user = super(RegistrationSerializer, self).create(validated_data)
        self.__notify_others(user)
        return validated_data

    def __notify_others(self, user):
        serializer = UserSerializer(user, many=False)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'notification', {
                'type': 'new_user_notification',
                'message': serializer.data
            }
        )
