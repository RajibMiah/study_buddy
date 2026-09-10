"""Write-side domain operations.

Views call these for anything that mutates state so the request handlers stay
thin and the business rules live in one place.
"""

from __future__ import annotations

from django.db import transaction

from .models import Message, Room, Topic, User, UserFollowing


@transaction.atomic
def create_room(*, host: User, name: str, description: str, topic_name: str,
                room_image=None) -> Room:
    topic, _ = Topic.objects.get_or_create(name=topic_name.strip())
    room = Room.objects.create(
        host=host,
        topic=topic,
        name=name.strip(),
        description=(description or "").strip(),
        room_image=room_image,
    )
    room.participants.add(host)
    return room


@transaction.atomic
def update_room(*, room: Room, name: str, description: str,
                topic_name: str) -> Room:
    topic, _ = Topic.objects.get_or_create(name=topic_name.strip())
    room.name = name.strip()
    room.description = (description or "").strip()
    room.topic = topic
    room.save(update_fields=["name", "description", "topic", "updated"])
    return room


@transaction.atomic
def post_message(*, room: Room, author: User, body: str) -> Message:
    body = body.strip()[:255]
    message = Message.objects.create(room=room, user=author, body=body)
    room.participants.add(author)
    return message


def delete_message(*, message: Message) -> int:
    room_id = message.room_id
    message.delete()
    return room_id


@transaction.atomic
def toggle_follow(*, follower: User, target: User) -> bool:
    """Follow ``target`` if not already following, else unfollow.

    Returns the resulting follow state (True == now following).
    """
    if follower == target:
        raise ValueError("Users cannot follow themselves.")
    existing = UserFollowing.objects.filter(
        user_id=follower, following_user_id=target
    )
    if existing.exists():
        existing.delete()
        return False
    UserFollowing.objects.create(user_id=follower, following_user_id=target)
    return True
