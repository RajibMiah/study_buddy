from base.models import Room, Topic, User, Vote
from rest_framework import serializers

# from stripe import Source

AVATOR_BASE_URL = 'http://127.0.0.1:8000/images/'


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
    total_vote = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Room
        fields = ['id', 'room_host',  'total_vote', 'topic', 'participants',
                  'name', 'description', 'updated', 'created']

    def get_participants(self, data):
        room = Room.objects.get(pk=data.pk)
        room_participants = room.participants.all()

        return SimpleUserSerializer(room_participants, many=True, read_only=True).data

    def get_total_vote(self, data):
        self.upvote = 0
        self.downvote = 0
        votes = Vote.objects.prefetch_related(
            'room').filter(room__id=data.id)
        for vote in votes:
            if (vote.upvote > 0):
                self.upvote += 1
            else:
                self.downvote += 1

        cumalative_vote = self.upvote - self.downvote
        return str(cumalative_vote)


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
