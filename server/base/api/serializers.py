
from base.models import Room, Topic
from rest_framework import serializers

# from stripe import Source


class SimpleUserSerializer(serializers.Serializer):
    name = serializers.CharField(read_only=True)
    avator = serializers.ImageField(read_only=True)
    uuid = serializers.UUIDField(read_only=True)


class RoomSerializer(serializers.ModelSerializer):
    participants = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Room
        fields = '__all__'

    def get_participants(self, data):
        room = Room.objects.prefetch_related('participants').get(pk=data.pk)
        room_participants = room.participants.all()
        return SimpleUserSerializer(room_participants, many=True).data


class TopicSerializer(serializers.ModelSerializer):
    total_rooms = serializers.SerializerMethodField()

    class Meta:
        model = Topic
        fields = '__all__'

    def get_total_rooms(self, obj):
        return obj.total_rooms
