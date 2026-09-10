from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .forms import RoomForm, StudyBuddyLoginForm, UserForm, UserRegisterForm
from .models import Message, Room, Topic, User, UserFollowing


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


@require_http_methods(["POST"])
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
        user = form.save()
        auth_login(request, user)
        messages.success(request, "Your account is ready.")
        return redirect("home")

    return render(
        request, "base/login.html", {"page": "register", "form": form}
    )


def userProfile(request, pk):
    user = get_object_or_404(User, pk=pk)
    context = {
        "user": user,
        "rooms": user.room_set.select_related("topic", "host"),
        "room_messages": user.message_set.select_related("room", "user"),
        "topics": Topic.objects.all(),
        "followers": UserFollowing.objects.filter(
            following_user_id=user
        ).count(),
    }
    return render(request, "base/profile.html", context)


def home(request):
    q = request.GET.get("q", "")

    rooms = (
        Room.objects.filter(
            Q(topic__name__icontains=q)
            | Q(name__icontains=q)
            | Q(host__username__icontains=q)
            | Q(description__icontains=q)
        )
        .select_related("host", "topic")
        .prefetch_related("participants")
    )
    room_messages = (
        Message.objects.filter(room__topic__name__icontains=q)
        .select_related("user", "room")
    )

    context = {
        "rooms": rooms,
        "topics": Topic.objects.all(),
        "room_count": rooms.count(),
        "room_messages": room_messages,
    }
    return render(request, "base/home.html", context)


@require_http_methods(["GET", "POST"])
def room(request, pk):
    room_details = get_object_or_404(
        Room.objects.select_related("host", "topic"), pk=pk
    )

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path())
        body = (request.POST.get("body") or "").strip()
        if body:
            Message.objects.create(
                user=request.user, room=room_details, body=body[:255]
            )
            room_details.participants.add(request.user)
        return redirect("room", pk=room_details.pk)

    context = {
        "room": room_details,
        "room_messages": room_details.message_set.select_related("user"),
        "participants": room_details.participants.all(),
    }
    return render(request, "base/room.html", context)


@login_required
@require_http_methods(["GET", "POST"])
def createRoom(request):
    form = RoomForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        room_obj = form.save(commit=False)
        room_obj.host = request.user
        room_obj.save()
        room_obj.participants.add(request.user)
        messages.success(request, "Room created.")
        return redirect("room", pk=room_obj.pk)

    return render(
        request,
        "base/room_form.html",
        {"form": form, "topics": Topic.objects.all()},
    )


@login_required
@require_http_methods(["GET", "POST"])
def updateRoom(request, pk):
    room_obj = get_object_or_404(Room, pk=pk)
    if request.user != room_obj.host:
        messages.error(request, "You can only edit rooms you host.")
        return redirect("room", pk=room_obj.pk)

    form = RoomForm(
        request.POST or None, request.FILES or None, instance=room_obj
    )
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Room updated.")
        return redirect("room", pk=room_obj.pk)

    return render(
        request,
        "base/room_form.html",
        {"form": form, "topics": Topic.objects.all(), "room": room_obj},
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
        room_id = message.room_id
        message.delete()
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


def topicsPage(request):
    q = request.GET.get("q", "")
    topics = Topic.objects.filter(name__icontains=q)
    return render(
        request,
        "base/topics.html",
        {"topics": topics, "total": Topic.objects.count()},
    )


def activityPage(request):
    room_messages = Message.objects.select_related(
        "user", "room", "room__topic"
    )[:50]
    return render(
        request, "base/activity.html", {"room_messages": room_messages}
    )
