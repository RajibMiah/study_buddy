from base.models import Room, User
from rest_framework import serializers


class SimplateRoomSerializer(serializers.ModelSerializer):

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
        user = User.objects.select_related('profile').get(pk=obj.pk)
        user_room_details = user.room_set.all()
        return SimplateRoomSerializer(user_room_details, many=True).data
