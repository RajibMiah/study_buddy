from urllib import request

from base.models import Message, Room, Topic, User, UserFollowing, Vote
from django.db.models import Sum
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


class VoteModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vote
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model: Message
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    participants = serializers.SerializerMethodField(read_only=True)
    room_host = SimpleUserSerializer(
        source='host', read_only=True)
    topic = SimpleTopicSerializer(read_only=True)
    # total_vote = serializers.SerializerMethodField(read_only=True)
    vote = serializers.SerializerMethodField(read_only=True)
    total_messages = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Room
        fields = ['id', 'room_host', 'room_image', 'topic', 'vote', 'participants', 'total_messages',
                  'name', 'description', 'updated', 'created']

    def create(self, validated_data):
        print('validated data', validated_data)
        print('requested user', self.user)
        return super().create(validated_data)

    def get_participants(self, data):
        room = Room.objects.select_related(
            'host', 'topic').get(pk=data.pk).participants.all()
        return SimpleUserSerializer(room, many=True, read_only=True).data

    def get_vote(self, data):
        votes = Vote.objects.select_related(
            'room', 'voted_room').filter(room__id=data.id).aggregate(Sum('upvote'), Sum('downvote'))

        return votes

    def get_total_messages(self, data):

        room_message = Message.objects.select_related('user', 'room').filter(
            room__id=data.pk).count()
        # print(room_message)

        return room_message
        # return MessageSerializer(room_message, many=True, read_only=True).data

    # def get_total_vote(self, data):
    #     self.upvote = 0
    #     self.downvote = 0
    #     votes = Vote.objects.select_related(
    #         'room', 'user').filter(room__id=data.id)
    #     for vote in votes:
    #         if (vote.upvote > 0):
    #             self.upvote += 1
    #         else:
    #             self.downvote += 1
    #     cumulative_vote = self.upvote - self.downvote
    #     return str(cumulative_vote)


class TopicSerializer(serializers.ModelSerializer):
    total_rooms = serializers.SerializerMethodField()

    class Meta:
        model = Topic
        fields = '__all__'

    def get_total_rooms(self, obj):
        return obj.total_rooms


class UserFollowingModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserFollowing
        fields = '__all__'
