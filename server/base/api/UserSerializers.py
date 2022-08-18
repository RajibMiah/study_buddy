

from base.models import Room, Skill, User, UserFollowing
from django.db.models import Count, Max
from rest_framework import serializers

from .serializers import RoomSerializer

AVATOR_BASE_URL = 'http://127.0.0.1:8000/images/'


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
            'designation',
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
        return RoomSerializer(user_room_details, many=True,  context=self.context).data

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


class SkillModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skill
        fields = '__all__'


class ProfileEditSerializer(serializers.ModelSerializer):

    skills = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'uuid', 'avator', 'designation', 'gender', 'location', 'github',
                  'linkedin', 'summary', 'birthday', 'date_joined', 'skills']
        depth = 2

    def get_skills(self, user):
        skills = Skill.objects.filter(user__id=user.id)

        return SkillModelSerializer(skills, many=True).data
