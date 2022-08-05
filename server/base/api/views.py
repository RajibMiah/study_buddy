
from base.models import Room, Topic, User
from rest_framework import viewsets

from .serializers import RoomSerializer, TopicSerializer, UserProfielSerializer

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

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TopicsModelViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    http_method_names = ['get']
