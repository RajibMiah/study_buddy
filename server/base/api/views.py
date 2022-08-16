

from multiprocessing import context
from urllib import request

from base.models import Room, Topic, User, UserFollowing, Vote
from django.db.models import Max, Min, Q
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response

from .serializers import (RoomSerializer, TopicSerializer,
                          UserFollowingModelSerializer, VoteModelSerializer)
from .UserSerializers import SimplateRoomSerializer, UserProfielSerializer


class UserProfileModelViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserProfielSerializer
    lookup_field = "uuid"
    http_method_names = ['get', 'patch', ]  # put
    parser_classes = (JSONParser, MultiPartParser, FormParser)

    def get_queryset(self):
        pk = self.kwargs.get("uuid")
        if pk is not None:
            return super().get_queryset()
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


class RoomModelViewSet(viewsets.ModelViewSet):

    queryset = Room.objects.select_related(
        'host', 'topic').annotate(voting_rank=Max('voted_room__upvote'), downvote=Min('voted_room__downvote')).order_by('-voting_rank', '-downvote', '-created', '-updated')
    serializer_class = RoomSerializer
    lookup_field = 'pk'
    # http_method_names = ['get', 'post' 'patch', ]
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly,
    #                       IsOwnerOrReadOnly]

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
        print('inside view create method')
        topic_name = request.data.pop('tags')
        print('pop topic name', topic_name)
        topic, created = Topic.objects.get_or_create(name=topic_name)

        context = request.data
        context['host'] = request.user.id
        context['topic'] = topic.id
        print('context ==========>', context)
        serializer = SimplateRoomSerializer(data=context)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            print('data is saved')
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        user = User.objects.get(room__id=pk)
        print('user', user)
        print('requested user', request.user)
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
    # http_method_names = ['get', 'patch']


class UserFollowingModelViewSet(viewsets.ModelViewSet):
    queryset = UserFollowing.objects.all()
    serializer_class = UserFollowingModelSerializer
    # http_method_names = ['get', 'patch', 'delete']
    # lookup_field = 'user_id'

    # def get_queryset(self):

    #         q = self.request.GET.get('user-id')
    #         if q is not None:
    #             room = super().get_queryset().filter(
    #                 Q(topic__name__icontains=q) |
    #                 Q(name__icontains=q) |
    #                 Q(host__username__icontains=q) |
    #                 Q(description__icontains=q)
    #             )
    #             return room
    #         return super().get_queryset()
