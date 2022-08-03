from base.models import Room, Topic
from pyexpat import model
from rest_framework import serializers
from stripe import Source


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class TopicSerializer(serializers.ModelSerializer):
    rooms = RoomSerializer(source='room_set', many=True)
    # print(rooms)
    # room_counter = serializers.SerializerMethodField()

    class Meta:
        model = Topic
        fields = '__all__'

    # def get_room_counter(self, obj):
    #     print("custom serializer", obj)
    #     return obj
