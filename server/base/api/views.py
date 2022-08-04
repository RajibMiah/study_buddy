
from base.models import Room, Topic, User
from rest_framework import generics, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response

from .serializers import RoomSerializer, TopicSerializer, UserProfielSerializer


@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/profile',
        'GET /api/topics',
        'GET /api/rooms',
        'GET /api/rooms/:id'
    ]
    return Response(routes)

# TODO:: RESOLVE ERROR ON USER PROFILE API


class UserProfile(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfielSerializer
    lookup_fields = 'pk'


class GetRooms(viewsets.ModelViewSet):

    queryset = Room.objects.all().order_by('?')
    serializer_class = RoomSerializer
    lookup_field = 'pk'
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly,
    #                       IsOwnerOrReadOnly]

    @action(detail=True)
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


@api_view(['GET'])
def getTopics(request):
    topic_instance = Topic.objects.all()
    serializers = TopicSerializer(topic_instance, many=True)
    return Response(serializers.data)


@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all().order_by('?')
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getRoom(request, pk):
    room = Room.objects.get(id=pk)
    serializer = RoomSerializer(room, many=False)
    return Response(serializer.data)
