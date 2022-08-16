from base.models import Room, User, UserFollowing
from rest_framework import serializers

from .serializers import RoomSerializer


class SimplateRoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = '__all__'


class UserFollowingStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollowing
        fields = '__all__'


class UserProfielSerializer(serializers.ModelSerializer):

    user_created_rooms = serializers.SerializerMethodField(read_only=True)
    follows_list = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'pk',
            'id',
            'uuid',
            'username',
            'name',
            'first_name',
            'last_name',
            'email',
            'bio',
            'avator',
            'follows_list',
            'user_created_rooms'
        )

    def get_user_created_rooms(self, obj):
        user = User.objects.select_related('profile').get(pk=obj.pk)
        user_room_details = user.room_set.all()
        return RoomSerializer(user_room_details, many=True).data

    def get_follows_list(self, data):
        requested_user_id = self.context['request'].user.id
        following_list = UserFollowing.objects.select_related('user_id').filter(
            user_id=data.id)
        ctx = dict()
        ctx['total_followers'] = following_list.count()
        ctx['is_followed'] = True if following_list.filter(
            following_user_id=requested_user_id) else False
        ctx['follows'] = UserFollowingStatusSerializer(
            following_list, many=True).data
        return ctx
