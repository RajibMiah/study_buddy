from base.models import Room, Topic, User, Vote
from rest_framework import serializers

# from stripe import Source

AVATOR_BASE_URL = 'http://127.0.0.1:8000/images/'


class SimpleVoteSerializer(serializers.Serializer):
    user = serializers.CharField(read_only=True)
    room = serializers.CharField(read_only=True)
    total_vote = serializers.IntegerField(read_only=True)


class SimpleUserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    username = serializers.CharField()
    uuid = serializers.UUIDField()
    avator = serializers.SerializerMethodField()

    def get_avator(self, user):
        if user.avator:
            avator_url = str(AVATOR_BASE_URL) + str(user.avator)
            return avator_url
        return None


class SimpleTopicSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class RoomSerializer(serializers.ModelSerializer):
    participants = serializers.SerializerMethodField(read_only=True)
    room_host = SimpleUserSerializer(
        source='host', read_only=True)
    topic = SimpleTopicSerializer(read_only=True)
    vote = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Room
        fields = ['id', 'room_host', 'vote', 'topic', 'participants',
                  'name', 'description', 'updated', 'created']
        deep = 1

    def get_participants(self, data):
        room = Room.objects.prefetch_related('voted_room').get(pk=data.pk)
        room_participants = room.participants.all()

        return SimpleUserSerializer(room_participants, many=True, read_only=True).data

    def get_vote(self,  data):

        user_voted_room = Vote.objects.filter(room__id=data.id)
        print('voted room', user_voted_room)

        return SimpleVoteSerializer(user_voted_room).data


class TopicSerializer(serializers.ModelSerializer):
    total_rooms = serializers.SerializerMethodField()

    class Meta:
        model = Topic
        fields = '__all__'

    def get_total_rooms(self, obj):
        return obj.total_rooms


class VoteModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vote
        fields = '__all__'
