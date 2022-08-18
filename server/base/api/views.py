

from base.models import Message, Room, Topic, User, UserFollowing, Vote
from django.db.models import Count, Max, Min, Q
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response

from .serializers import (MessageModelSerializer,
                          MostFollowedUserModelSerializer, RoomSerializer,
                          TopicSerializer, UserFollowingModelSerializer,
                          VoteModelSerializer)
from .UserSerializers import (ProfileEditSerializer, SimplateRoomSerializer,
                              UserProfielSerializer)


class UserProfileModelViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserProfielSerializer
    lookup_field = "uuid"
    http_method_names = ['get', 'patch', ]  # put
    parser_classes = (JSONParser, MultiPartParser, FormParser)

    def get_queryset(self):
        pk = self.kwargs.get("uuid")
        if pk is not None:
            return super().get_queryset().filter(uuid=pk)
        return User.objects.none()

    @action(detail=True, methods=['patch', 'put'])
    def avator(self, reqeust, pk=None):
        print('user pk', pk)
        user = self.get_object()
        serializer = UserProfielSerializer(
            user, reqeust.data, context={'request': self.request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)


class UserEditProfileModelViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = ProfileEditSerializer
    lookup_field = "uuid"
    http_method_names = ['get', 'patch', ]  # put
    # def get_queryset(self):
    #     pk = self.kwargs.get("uuid")
    #     if pk is not None:
    #         print('user pk is', pk)
    #         return super().get_queryset().get(uuid=pk)
    #     return User.objects.none()


class RoomModelViewSet(viewsets.ModelViewSet):

    queryset = Room.objects.select_related(
        'host', 'topic').annotate(voting_rank=Max('voted_room__upvote'), downvote=Min('voted_room__downvote')).order_by('-voting_rank', '-downvote', '-created', '-updated')
    serializer_class = RoomSerializer
    lookup_field = 'pk'

    def get_queryset(self):

        q = self.request.GET.get('q')
        if q is not None:
            room = super().get_queryset().filter(
                Q(topic__name__icontains=q) |
                Q(name__icontains=q) |
                Q(host__username__icontains=q) |
                Q(description__icontains=q)
            )
            return room
        return super().get_queryset()

    def create(self, request, *args, **kwargs):
        print('inside view create method', request.data)
        request.data._mutable = True
        topic_name = request.data.pop('tags')
        for topic in topic_name:
            topic, created = Topic.objects.get_or_create(name=topic)
        context = request.data
        context['host'] = request.user.id
        context['topic'] = topic.id
        serializer = SimplateRoomSerializer(data=context)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        user = User.objects.get(room__id=pk)
        if user == request.user:
            return super().update(request, *args, **kwargs)
        return Response({'msg': 'You are not authorized for update'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        user = User.objects.get(room__id=pk)

        if user == request.user:
            return super().destroy(request, *args, **kwargs)
        return Response({'msg': 'You are not authorized for delete this room'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch', 'put'])
    def room_image(self, reqeust, pk=None):
        print('room pk', pk)
        room = self.get_object(id=pk)
        serializer = RoomSerializer(room, reqeust.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)


class TopicsModelViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    http_method_names = ['get']


class VoteModelViewSet(viewsets.ModelViewSet):

    queryset = Vote.objects.all()
    serializer_class = VoteModelSerializer


class UserFollowingModelViewSet(viewsets.ModelViewSet):
    queryset = UserFollowing.objects.all()
    serializer_class = UserFollowingModelSerializer


class MostFollowedPeopleModelViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('?')
    serializer_class = MostFollowedUserModelSerializer
    http_method_names = ['get']

    def get_queryset(self):
        # print('requested id', self.request.user.id)
        # users = UserFollowing.objects.filter(
        #     following_user_id=self.request.user.id)
        # print("users", users)
        not_followed_by_user = super().get_queryset().exclude(
            followers=self.request.user.id)
        # print(not_followed_by_user)
        return not_followed_by_user
