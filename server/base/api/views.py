
from base.models import Room, Topic, User
from rest_framework import status, viewsets
from rest_framework.response import Response

from .serializers import RoomSerializer, TopicSerializer
from .UserSerializers import UserProfielSerializer

# @api_view(['GET'])
# def getRoutes(request):
#     routes = [
#         'GET /api',
#         # 'GET /api/profile',
#         'GET /api/topics',
#         'GET /api/rooms',
#         'GET /api/rooms/:id'
#     ]
#     return Response(routes)


class UserProfileModelViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserProfielSerializer
    lookup_field = 'pk'
    http_method_names = ['get', 'put', ]

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        if pk is not None:
            return super().get_queryset()
        return User.objects.none()


class RoomModelViewSet(viewsets.ModelViewSet):

    queryset = Room.objects.all().order_by('?')
    serializer_class = RoomSerializer
    lookup_field = 'pk'
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly,
    #                       IsOwnerOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        user = User.objects.get(room__id=pk)

        if user == request.user:
            return super().destroy(request, *args, **kwargs)
        return Response({'msg': 'You are not authorized for delete this room'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        user = User.objects.get(room__id=pk)

        if user == request.user:
            return super().destroy(request, *args, **kwargs)
        return Response({'msg': 'You are not authorized for update'}, status=status.HTTP_400_BAD_REQUEST)


class TopicsModelViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    http_method_names = ['get']
