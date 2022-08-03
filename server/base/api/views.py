
from base.models import Room, Topic
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import RoomSerializer, TopicSerializer


@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/topics',
        'GET /api/rooms',
        'GET /api/rooms/:id'
    ]
    return Response(routes)


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
