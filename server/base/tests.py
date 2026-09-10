from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test.utils import CaptureQueriesContext
from django.db import connection
from django.urls import reverse

from base.models import Message, Room, Topic, UserFollowing

User = get_user_model()


class AuthFlowTests(TestCase):
    def test_registration_hashes_password_and_logs_in(self):
        resp = self.client.post(
            reverse("register"),
            {
                "name": "Cara",
                "username": "Cara",
                "email": "cara@example.com",
                "password1": "spinning-otter-42",
                "password2": "spinning-otter-42",
            },
        )
        self.assertRedirects(resp, reverse("home"))
        user = User.objects.get(username="cara")  # normalised to lowercase
        self.assertTrue(user.has_usable_password())
        self.assertNotEqual(user.password, "spinning-otter-42")
        self.assertTrue(user.check_password("spinning-otter-42"))

    def test_logout_requires_post(self):
        self.assertEqual(self.client.get(reverse("logout")).status_code, 405)

    def test_create_room_requires_login(self):
        resp = self.client.get(reverse("create-room"))
        self.assertEqual(resp.status_code, 302)
        self.assertIn(reverse("login"), resp["Location"])


class RoomPermissionTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user("owner", password="pw-owner-123")
        self.other = User.objects.create_user("other", password="pw-other-123")
        self.topic = Topic.objects.create(name="Python")
        self.room = Room.objects.create(
            host=self.owner, topic=self.topic, name="Owned room"
        )

    def test_non_host_cannot_edit_room(self):
        self.client.force_login(self.other)
        resp = self.client.post(
            reverse("update-room", args=[self.room.pk]),
            {"name": "Hijacked", "topic_name": "Python", "description": ""},
        )
        self.assertRedirects(resp, reverse("room", args=[self.room.pk]))
        self.room.refresh_from_db()
        self.assertEqual(self.room.name, "Owned room")

    def test_non_host_cannot_delete_room(self):
        self.client.force_login(self.other)
        self.client.post(reverse("delete-room", args=[self.room.pk]))
        self.assertTrue(Room.objects.filter(pk=self.room.pk).exists())

    def test_anonymous_message_post_is_rejected(self):
        resp = self.client.post(
            reverse("room", args=[self.room.pk]), {"body": "hi"}
        )
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Message.objects.count(), 0)

    def test_author_only_message_delete(self):
        msg = Message.objects.create(
            room=self.room, user=self.owner, body="mine"
        )
        self.client.force_login(self.other)
        self.client.post(reverse("delete-message", args=[msg.pk]))
        self.assertTrue(Message.objects.filter(pk=msg.pk).exists())


class QueryBudgetTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        for i in range(25):
            host = User.objects.create_user(f"u{i}", password="pw-1234567")
            topic = Topic.objects.create(name=f"T{i}")
            room = Room.objects.create(host=host, topic=topic, name=f"R{i}")
            room.participants.add(host)
            Message.objects.create(room=room, user=host, body=f"m{i}")

    def test_home_query_count_is_bounded(self):
        with CaptureQueriesContext(connection) as ctx:
            self.assertEqual(self.client.get(reverse("home")).status_code, 200)
        self.assertLess(len(ctx.captured_queries), 8)

    def test_topics_query_count_is_bounded(self):
        with CaptureQueriesContext(connection) as ctx:
            self.client.get(reverse("topics"))
        self.assertLess(len(ctx.captured_queries), 5)


class FollowServiceTests(TestCase):
    def setUp(self):
        self.a = User.objects.create_user("aa", password="pw-1234567")
        self.b = User.objects.create_user("bb", password="pw-1234567")

    def test_toggle_follow_round_trip(self):
        self.client.force_login(self.a)
        url = reverse("toggle-follow", args=[self.b.pk])
        self.client.post(url)
        self.assertTrue(
            UserFollowing.objects.filter(
                user_id=self.a, following_user_id=self.b
            ).exists()
        )
        self.client.post(url)
        self.assertFalse(
            UserFollowing.objects.filter(
                user_id=self.a, following_user_id=self.b
            ).exists()
        )

    def test_cannot_follow_self(self):
        self.client.force_login(self.a)
        self.client.post(reverse("toggle-follow", args=[self.a.pk]))
        self.assertEqual(UserFollowing.objects.count(), 0)
