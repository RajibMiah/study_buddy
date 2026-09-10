"""Read-side query helpers.

Every function returns a queryset (or scalar) with eager loading and
annotations already applied, so views and templates never trigger per-row
follow-up queries.
"""

from __future__ import annotations

from django.db.models import Count, Q, QuerySet

from .models import Message, Room, Topic, User, UserFollowing


def _room_search_q(query: str) -> Q:
    return (
        Q(topic__name__icontains=query)
        | Q(name__icontains=query)
        | Q(host__username__icontains=query)
        | Q(description__icontains=query)
    )


def search_rooms(query: str = "") -> QuerySet[Room]:
    """Rooms matching ``query``, with host/topic joined and counts annotated."""
    qs = Room.objects.select_related("host", "topic")
    if query:
        qs = qs.filter(_room_search_q(query))
    return qs.annotate(
        participant_count=Count("participants", distinct=True),
        message_count=Count("message", distinct=True),
    ).order_by("-updated", "-created")


def room_detail_qs() -> QuerySet[Room]:
    """Base queryset for a room page: host/topic joined, participants counted.

    Pass to ``get_object_or_404`` so a missing id is a clean 404.
    """
    return Room.objects.select_related("host", "topic").annotate(
        participant_count=Count("participants", distinct=True)
    )


def room_messages(room_id: int) -> QuerySet[Message]:
    return (
        Message.objects.filter(room_id=room_id)
        .select_related("user")
        .order_by("created")
    )


def room_participants(room: Room) -> QuerySet[User]:
    return room.participants.only(
        "id", "username", "name", "avator"
    ).order_by("username")


def recent_activity(query: str = "", limit: int = 50) -> QuerySet[Message]:
    qs = Message.objects.select_related("user", "room", "room__topic")
    if query:
        qs = qs.filter(room__topic__name__icontains=query)
    return qs.order_by("-created")[:limit]


def list_topics(query: str = "", limit: int | None = None) -> QuerySet[Topic]:
    qs = Topic.objects.annotate(num_rooms=Count("room"))
    if query:
        qs = qs.filter(name__icontains=query)
    qs = qs.order_by("-num_rooms", "name")
    return qs[:limit] if limit else qs


def profile_rooms(user: User) -> QuerySet[Room]:
    return (
        user.room_set.select_related("topic", "host")
        .annotate(participant_count=Count("participants", distinct=True))
        .order_by("-updated")
    )


def profile_messages(user: User, limit: int = 30) -> QuerySet[Message]:
    return user.message_set.select_related("room", "room__topic").order_by(
        "-created"
    )[:limit]


def follower_count(user: User) -> int:
    return UserFollowing.objects.filter(following_user_id=user).count()


def is_following(*, follower: User, target: User) -> bool:
    if not follower.is_authenticated:
        return False
    return UserFollowing.objects.filter(
        user_id=follower, following_user_id=target
    ).exists()
