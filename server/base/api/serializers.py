

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


class MessageModelSerializer(serializers.ModelSerializer):
    user_details = SimpleUserSerializer(source='user', read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'user', 'room', 'body', 'created', 'user_details']


class RoomSerializer(serializers.ModelSerializer):
    participants = serializers.SerializerMethodField(read_only=True)
    room_host = SimpleUserSerializer(
        source='host', read_only=True)
    topic = SimpleTopicSerializer(read_only=True)
    vote = serializers.SerializerMethodField(read_only=True)
    messages = serializers.SerializerMethodField(read_only=True)
    is_votted = serializers.SerializerMethodField(read_only=True)
    room_image = serializers.SerializerMethodField('get_room_image')
    is_joined = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = ['id', 'room_host', 'room_image', 'topic', 'vote', 'is_votted', 'participants', 'messages',
                  'name', 'description', 'updated', 'created', 'is_joined']

    def get_participants(self, data):
        room = Room.objects.select_related(
            'host', 'topic').get(pk=data.pk).participants.all()
        return SimpleUserSerializer(room, many=True, read_only=True).data

    def get_vote(self, data):
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
        vote = Vote.objects.filter(
            Q(room_id=data.id), Q(user=self.context['request'].user.id))
        return SimpleVoteSerializer(vote, many=True).data

    def get_messages(self, data):
        room_message_set = Message.objects.select_related('user', 'room').filter(
            room__id=data.pk)
        ctx = dict()
        ctx['total_messages'] = room_message_set.count()
        ctx['message_set'] = MessageModelSerializer(
            room_message_set, many=True).data
        return ctx

    def get_room_image(self, obj):
        if obj.room_image:
            image_url = str(AVATOR_BASE_URL) + str(obj.room_image)
            return image_url
        return None

    def get_is_joined(self, obj):
        qs = Room.objects.prefetch_related('participants').filter(
            Q(id=obj.pk), Q(participants=self.context['request'].user.id))
        return qs.exists()


class TopicSerializer(serializers.ModelSerializer):
    total_rooms = serializers.SerializerMethodField()

    class Meta:
        model = Topic
        fields = '__all__'

    def get_total_rooms(self, obj):
        return obj.total_rooms


class UserFollowingModelSerializer(serializers.ModelSerializer):
    # user = SimpleUserSerializer(source='user_id')
    total_follower = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = UserFollowing
        fields = "__all__"

    def get_total_follower(self, user):
        followers = UserFollowing.objects.filter(user_id=user.id).count()
        return followers


class TopProfileModelSerializer(serializers.ModelSerializer):
    is_followed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'name', 'username', 'avator',
                  'designation', 'uuid', 'is_followed')

    def get_is_followed(self, obj):
        follwed_user = UserFollowing.objects.filter(Q(user_id=obj.id), Q(
            following_user_id=self.context['request'].user.id))

        return follwed_user.exists()
    # class MostFollowedUserModelSerializer(serializers.ModelSerializer):

    #     class Meta:
    #         model = UserFollowing
    #         fields = ('id', 'user', 'following_user_id')
    # depth = 1
    # id = serializers.IntegerField(read_only=True)
    # username = serializers.CharField(read_only=True)
    # name = serializers.CharField(read_only=True)
    # total_follower = serializers.SerializerMethodField(read_only=True)
    # uuid = serializers.UUIDField(read_only=True)
    # designation = serializers.CharField(read_only=True)

    # avator = serializers.SerializerMethodField(read_only=True)

    # def get_avator(self, user):
    #     if user.avator:
    #         avator_url = str(AVATOR_BASE_URL) + str(user.avator)
    #         return avator_url
    #     return None
