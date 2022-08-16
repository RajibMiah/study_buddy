
from base.models import Message, Room, Topic, User, UserFollowing, Vote
from django.db.models import Q, Sum
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


class SimpleVoteSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    room = serializers.PrimaryKeyRelatedField(read_only=True)
    upvote_boolean = serializers.BooleanField(read_only=True)
    downvote_boolean = serializers.BooleanField(read_only=True)


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
    is_votted = serializers.SerializerMethodField(read_only=True)
    room_image = serializers.SerializerMethodField('get_room_image')

    class Meta:
        model = Room
        fields = ['id', 'room_host', 'room_image', 'topic', 'vote', 'is_votted', 'participants', 'total_messages',
                  'name', 'description', 'updated', 'created']

    def get_participants(self, data):
        room = Room.objects.select_related(
            'host', 'topic').get(pk=data.pk).participants.all()
        return SimpleUserSerializer(room, many=True, read_only=True).data

    def get_vote(self, data):
        # requested_id = self.context['request'].user.id
        votes = Vote.objects.select_related(
            'room', 'user').filter(room__id=data.id)
        agg_vote = votes.aggregate(Sum('upvote'), Sum('downvote'))
        vote_list = SimpleVoteSerializer(votes, many=True).data

        context = dict()
        context['upvote'] = agg_vote['upvote__sum']
        context['downvote'] = agg_vote['downvote__sum']
        context['vote_list'] = vote_list

        return context

    def get_is_votted(self, data):
        # requested_id = self.context['request'].user.
        # print('requested id', requested_id, 'data user id', data.id)
        vote = Vote.objects.filter(
            Q(room_id=data.id), Q(user=self.context['request'].user.id))
        return SimpleVoteSerializer(vote, many=True).data

    def get_total_messages(self, data):

        room_message = Message.objects.select_related('user', 'room').filter(
            room__id=data.pk).count()
        # print(room_message)

        return room_message
        # return MessageSerializer(room_message, many=True, read_only=True).data

    def get_room_image(self, obj):
        if obj.room_image:
            image_url = str(AVATOR_BASE_URL) + str(obj.room_image)
            return image_url
        return None

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
