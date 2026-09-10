from base.models import Message, Room, Topic, User, UserFollowing, Vote
from django.db.models import Count, Max, Min, Q
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from .serializers import (MessageModelSerializer, RoomSerializer,
                          TopicSerializer, TopProfileModelSerializer,
                          UserFollowingModelSerializer, VoteModelSerializer)
from .UserSerializers import (ProfileEditSerializer, SimplateRoomSerializer,
                              UserProfielSerializer)


class UserProfileModelViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserProfielSerializer
    lookup_field = "uuid"
    http_method_names = ["get", "patch"]
    permission_classes = [IsAuthenticated]
    parser_classes = (JSONParser, MultiPartParser, FormParser)

    def get_queryset(self):
        return User.objects.select_related("profile")

    def get_object(self):
        obj = get_object_or_404(
            self.get_queryset(), uuid=self.kwargs.get("uuid")
        )
        return obj

    def partial_update(self, request, *args, **kwargs):
        if self.get_object() != request.user:
            return Response(
                {"detail": "You can only edit your own profile."},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().partial_update(request, *args, **kwargs)

    @action(detail=True, methods=["patch"])
    def avator(self, request, uuid=None):
        user = self.get_object()
        if user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(user, request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserEditProfileModelViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = ProfileEditSerializer
    lookup_field = "uuid"
    http_method_names = ["get", "patch"]
    permission_classes = [IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        if self.get_object() != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().partial_update(request, *args, **kwargs)


class RoomModelViewSet(viewsets.ModelViewSet):

    serializer_class = RoomSerializer
    lookup_field = "pk"
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = (
            Room.objects.select_related("host", "topic")
            .prefetch_related("participants")
            .annotate(
                voting_rank=Max("voted_room__upvote"),
                downvote=Min("voted_room__downvote"),
            )
            .order_by("-voting_rank", "-downvote", "-created", "-updated")
        )
        q = self.request.query_params.get("q")
        if q:
            qs = qs.filter(
                Q(topic__name__icontains=q)
                | Q(name__icontains=q)
                | Q(host__username__icontains=q)
                | Q(description__icontains=q)
            )
        return qs

    def _require_host(self):
        if self.get_object().host_id != self.request.user.id:
            return Response(
                {"detail": "You do not own this room."},
                status=status.HTTP_403_FORBIDDEN,
            )
        return None

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        tags = data.pop("tags", None) or []
        if isinstance(tags, str):
            tags = [tags]
        topic = None
        for tag in tags:
            topic, _ = Topic.objects.get_or_create(name=str(tag).strip())
        if topic is None:
            return Response(
                {"tags": "At least one topic is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        data["host"] = request.user.id
        data["topic"] = topic.id
        serializer = SimplateRoomSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        room = serializer.save()
        room.participants.add(request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        denied = self._require_host()
        return denied or super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        denied = self._require_host()
        return denied or super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        denied = self._require_host()
        return denied or super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=["patch"])
    def room_image(self, request, pk=None):
        denied = self._require_host()
        if denied:
            return denied
        serializer = self.get_serializer(
            self.get_object(), request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class TopicsModelViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.annotate(num_rooms=Count("room"))
    serializer_class = TopicSerializer
    http_method_names = ["get"]
    permission_classes = [IsAuthenticatedOrReadOnly]


class VoteModelViewSet(viewsets.ModelViewSet):

    serializer_class = VoteModelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Vote.objects.filter(user=self.request.user).select_related(
            "room", "user"
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class UserFollowingModelViewSet(viewsets.ModelViewSet):
    serializer_class = UserFollowingModelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserFollowing.objects.filter(
            user_id=self.request.user
        ).select_related("user_id", "following_user_id")

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)


class TopProfileModelViewSet(viewsets.ModelViewSet):
    serializer_class = TopProfileModelSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    def get_queryset(self):
        return (
            User.objects.exclude(id=self.request.user.id)
            .annotate(followers_total=Count("followers"))
            .order_by("-followers_total")
        )


class MessageModelViewSet(viewsets.ModelViewSet):
    serializer_class = MessageModelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Message.objects.select_related("user", "room").order_by("created")
        room_id = self.request.query_params.get("room")
        return qs.filter(room_id=room_id) if room_id else qs.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def addORRemoveParticipants(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if room.participants.filter(pk=request.user.pk).exists():
        room.participants.remove(request.user)
        return Response({"msg": "user removed"}, status=status.HTTP_200_OK)
    room.participants.add(request.user)
    return Response({"msg": "user added"}, status=status.HTTP_200_OK)
