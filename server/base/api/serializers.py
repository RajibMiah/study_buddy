
from base.models import Room, Topic, User
from rest_framework import serializers

# from stripe import Source


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class UserProfielSerializer(serializers.ModelSerializer):

    user_created_rooms = serializers.SerializerMethodField(read_only=True)

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
            'user_created_rooms'
        )

    def get_user_created_rooms(self, obj):
        user = User.objects.get(pk=obj.pk)
        user_room_details = user.room_set.all()
        return RoomSerializer(user_room_details, many=True).data


class TopicSerializer(serializers.ModelSerializer):
    total_rooms = serializers.SerializerMethodField()

    class Meta:
        model = Topic
        fields = '__all__'

    def get_total_rooms(self, obj):
        return obj.total_rooms
