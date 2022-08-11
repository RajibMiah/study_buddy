
from base.models import Room, Topic, User, Vote
from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.response import Response

from .serializers import RoomSerializer, TopicSerializer, VoteModelSerializer
from .UserSerializers import UserProfielSerializer


class UserProfileModelViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserProfielSerializer
    lookup_field = "uuid"
    http_method_names = ['get', 'patch', ]  # put

    def get_queryset(self):
        pk = self.kwargs.get("uuid")
        if pk is not None:
            return super().get_queryset()
        return User.objects.none()


class RoomModelViewSet(viewsets.ModelViewSet):

    queryset = Room.objects.all().order_by('?')
    serializer_class = RoomSerializer
    lookup_field = 'pk'
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


class TopicsModelViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    http_method_names = ['get']


class VoteModelViewSet(viewsets.ModelViewSet):

    queryset = Vote.objects.all()
    serializer_class = VoteModelSerializer
    http_method_names = ['get', 'patch', ]
