from base.models import Room, Topic
from pyexpat import model
from rest_framework.serializers import ModelSerializer
from stripe import Source


class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class TopicSerializer(ModelSerializer):
    rooms = RoomSerializer(source='room_set', many=True)
    print(rooms)

    class Meta:
        model = Topic
        fields = '__all__'
