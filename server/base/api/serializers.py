
from base.models import Room, Topic
from rest_framework import serializers

# from stripe import Source

AVATOR_BASE_URL = 'http://127.0.0.1:8000/images/'


class SimpleUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    username = serializers.CharField(read_only=True)
    uuid = serializers.UUIDField(read_only=True)
    avator = serializers.SerializerMethodField(read_only=True)

    def get_avator(self, user):
        if user.avator:
            avator_url = str(AVATOR_BASE_URL) + str(user.avator)
            return avator_url
        return None


class SimpleTopicSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)


class RoomSerializer(serializers.ModelSerializer):
    participants = serializers.SerializerMethodField(read_only=True)
    room_host = SimpleUserSerializer(
        source='host', read_only=True)
    topic = SimpleTopicSerializer(read_only=True)

    class Meta:
        model = Room
        fields = ['id', 'room_host', 'topic', 'participants',
                  'name', 'description', 'updated', 'created']

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
