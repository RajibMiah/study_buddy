
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.shortcuts import HttpResponse, redirect, render

from .forms import RoomForm, UserForm, UserRegisterFrom
from .models import Message, Room, Topic, User, UserFollowing

# Create your views here.


def login(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
            print("user found", user)
        except:
            messages.error(request, 'User does not exist')
            print('user does not exist')
        print("username", username, 'passwrod', password)
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            messages.success(
                request, 'Login successfull . Redirect to home page')
            return redirect('home')
        else:
            print('username and password does not match')
            messages.error(request, 'Username OR password does not exit')

    context = {'page': page}
    return render(request, 'base/login.html', context)


def logout(request):
    auth_logout(request)
    return redirect('home')


def registerPage(request):

    if request.user.is_authenticated:
        return redirect('home')

    page = 'register'
    form = UserRegisterFrom()
    if request.method == 'POST':
        form = UserRegisterFrom(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            auth_login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'An error occured during registration!')

    context = {'page': page, 'form': form}
    return render(request, 'base/login.html', context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topic = Topic.objects.all()
    followers = UserFollowing.objects.filter(following_user_id=pk)
    context = {'user': user, 'rooms': rooms,
               'room_messages': room_messages, 'topics': topic, 'followers': followers.count()}
    # print(context)
    return render(request, 'base/profile.html', context)


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    room = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(host__username__icontains=q) |
        Q(description__icontains=q)
    )
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    topic = Topic.objects.all()
    room_count = room.count()
    context = {"rooms": room, 'topics': topic,
               'room_count': room_count, 'room_messages': room_messages}

    return render(request, 'base/home.html', context)


def room(request, pk):

    room_details = Room.objects.get(id=pk)
    room_messages = room_details.message_set.all()
    participants = room_details.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room_details,
            body=request.POST.get('body')
        )
    room_details.participants.add(request.user)
    context = {'room': room_details, 'room_messages': room_messages,
               'participants': participants}
    return render(request, "base/room.html", context)


@login_required(login_url='/login')
def createRoom(request):
    form = RoomForm
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        form = RoomForm(request.POST)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )
        return redirect('home')

    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='/login')
def updateRoom(request, pk):

    room = Room.objects.get(id=pk)
    topics = Topic.objects.all()
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('You are not allowed here to updated room!!!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context = {'form': form, 'topics': topics}

    return render(request, 'base/room_form.html', context)


@login_required(login_url='/login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You are not allowed here to updated room!!!')

    if request.method == 'POST':
        room.delete()
        return redirect('home')

    context = {'obj': room}
    return render(request, 'base/delete.html', context)


@login_required(login_url='/login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse('You are not allowed here !!')
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    context = {'obj': message}
    return render(request, 'base/delete.html', context)


@login_required(login_url='/login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid:
            form.save()
            return redirect('user-profile', pk=user.id)

    context = {'form': form}
    return render(request, 'base/update_user.html', context)


def topicsPage(request):
    return HttpResponse('Topic page')


def activityPage(request):
    return HttpResponse('activity page')
