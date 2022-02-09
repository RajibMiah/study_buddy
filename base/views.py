
from urllib import request
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Q
from .models import Room, Topic , Message
from .forms import RoomForm


# Create your views here.


def login(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('home')

        except:
            messages.error(request, 'Something  went worng')

        user = authenticate(request, username=username, password=password)

    context = {'page': page}
    return render(request, 'base/login.html', context)


def logout(request):
    auth_logout(request)
    return redirect('home')


def registerPage(request):
    
    if request.user.is_authenticated:
        return redirect('home')

    page = 'register'
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
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


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    room = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(host__username__icontains=q) |
        Q(description__icontains=q)
    )

    topic = Topic.objects.all()
    room_count = room.count()
    context = {"rooms": room, 'topics': topic, 'room_count': room_count}

    return render(request, 'base/home.html', context)


def room(request, pk):

    room_details = Room.objects.get(id=pk)
    room_messages = room_details.message_set.all().order_by('-created')
    participants = room_details.participants.all()
    print('participants' , participants)
    if request.method == 'POST':

        message = Message.objects.create(
            user = request.user,
            room = room_details,
            body = request.POST.get('body')

        )
        room_details.participants.add(request.user)
        print('message body' , message)
        return redirect('room' , pk = room_details.id)

    context = {'room': room_details , 'room_messages': room_messages , 'participants':participants}
    return render(request, "base/room.html", context)


@login_required(login_url='/login')
def createRoom(request):
    form = RoomForm
    if request.method == 'POST':
        form = RoomForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='/login')
def updateRoom(request, pk):

    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('You are not allowed here to updated room!!!')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}

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
