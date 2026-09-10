from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods, require_POST

from . import selectors, services
from .forms import RoomForm, StudyBuddyLoginForm, UserForm, UserRegisterForm
from .models import Message, Room, User


@require_http_methods(["GET", "POST"])
def login(request):
    if request.user.is_authenticated:
        return redirect("home")

    form = StudyBuddyLoginForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        auth_login(request, form.get_user())
        messages.success(request, "Welcome back!")
        return redirect(request.GET.get("next") or "home")

    return render(request, "base/login.html", {"page": "login", "form": form})


@require_POST
def logout(request):
    auth_logout(request)
    messages.info(request, "You have been signed out.")
    return redirect("home")


@require_http_methods(["GET", "POST"])
def registerPage(request):
    if request.user.is_authenticated:
        return redirect("home")

    form = UserRegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        auth_login(request, form.save())
        messages.success(request, "Your account is ready.")
        return redirect("home")

    return render(
        request, "base/login.html", {"page": "register", "form": form}
    )


def home(request):
    q = request.GET.get("q", "")
    rooms = selectors.search_rooms(q)
    context = {
        "rooms": rooms,
        "topics": selectors.list_topics(),
        "room_count": rooms.count(),
        "room_messages": selectors.recent_activity(q),
    }
    return render(request, "base/home.html", context)


@require_http_methods(["GET", "POST"])
def room(request, pk):
    room_obj = get_object_or_404(selectors.room_detail_qs(), pk=pk)

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path())
        body = request.POST.get("body", "")
        if body.strip():
            services.post_message(
                room=room_obj, author=request.user, body=body
            )
        return redirect("room", pk=room_obj.pk)

    context = {
        "room": room_obj,
        "room_messages": selectors.room_messages(pk),
        "participants": selectors.room_participants(room_obj),
    }
    return render(request, "base/room.html", context)


def userProfile(request, pk):
    profile = get_object_or_404(User, pk=pk)
    context = {
        "user": profile,
        "rooms": selectors.profile_rooms(profile),
        "room_messages": selectors.profile_messages(profile),
        "topics": selectors.list_topics(),
        "followers": selectors.follower_count(profile),
        "is_following": selectors.is_following(
            follower=request.user, target=profile
        ),
    }
    return render(request, "base/profile.html", context)


@login_required
@require_http_methods(["GET", "POST"])
def createRoom(request):
    form = RoomForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        room_obj = services.create_room(
            host=request.user,
            room_image=form.cleaned_data.get("room_image"),
            **_room_fields(form),
        )
        messages.success(request, "Room created.")
        return redirect("room", pk=room_obj.pk)

    return render(
        request,
        "base/room_form.html",
        {"form": form, "topics": selectors.list_topics()},
    )


@login_required
@require_http_methods(["GET", "POST"])
def updateRoom(request, pk):
    room_obj = get_object_or_404(Room, pk=pk)
    if request.user != room_obj.host:
        messages.error(request, "You can only edit rooms you host.")
        return redirect("room", pk=room_obj.pk)

    form = RoomForm(request.POST or None, instance=room_obj)
    if request.method == "POST" and form.is_valid():
        services.update_room(room=room_obj, **_room_fields(form))
        messages.success(request, "Room updated.")
        return redirect("room", pk=room_obj.pk)

    return render(
        request,
        "base/room_form.html",
        {"form": form, "topics": selectors.list_topics(), "room": room_obj},
    )


@login_required
@require_http_methods(["GET", "POST"])
def deleteRoom(request, pk):
    room_obj = get_object_or_404(Room, pk=pk)
    if request.user != room_obj.host:
        messages.error(request, "You can only delete rooms you host.")
        return redirect("room", pk=room_obj.pk)

    if request.method == "POST":
        room_obj.delete()
        messages.success(request, "Room deleted.")
        return redirect("home")

    return render(request, "base/delete.html", {"obj": room_obj})


@login_required
@require_http_methods(["GET", "POST"])
def deleteMessage(request, pk):
    message = get_object_or_404(Message.objects.select_related("room"), pk=pk)
    if request.user != message.user:
        messages.error(request, "You can only delete your own messages.")
        return redirect("room", pk=message.room_id)

    if request.method == "POST":
        room_id = services.delete_message(message=message)
        messages.success(request, "Message deleted.")
        return redirect("room", pk=room_id)

    return render(request, "base/delete.html", {"obj": message})


@login_required
@require_http_methods(["GET", "POST"])
def updateUser(request):
    form = UserForm(
        request.POST or None, request.FILES or None, instance=request.user
    )
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Profile updated.")
        return redirect("user-profile", pk=request.user.pk)

    return render(request, "base/update_user.html", {"form": form})


@login_required
@require_POST
def toggleFollow(request, pk):
    target = get_object_or_404(User, pk=pk)
    try:
        now_following = services.toggle_follow(
            follower=request.user, target=target
        )
    except ValueError as exc:
        messages.error(request, str(exc))
    else:
        messages.success(
            request,
            f"You are now following {target.username}."
            if now_following
            else f"You unfollowed {target.username}.",
        )
    return redirect("user-profile", pk=target.pk)


def topicsPage(request):
    q = request.GET.get("q", "")
    return render(
        request,
        "base/topics.html",
        {"topics": selectors.list_topics(q), "total": selectors.list_topics().count()},
    )


def activityPage(request):
    return render(
        request,
        "base/activity.html",
        {"room_messages": selectors.recent_activity(request.GET.get("q", ""))},
    )


def _room_fields(form):
    return {
        "name": form.cleaned_data["name"],
        "description": form.cleaned_data.get("description", ""),
        "topic_name": form.cleaned_data["topic_name"],
    }
