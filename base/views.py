
from django.shortcuts import render
from .models import Room 
import json

# Create your views here.

 
def home(request):
    room = Room.objects.all()
    context = {"rooms": room}
    return render(request , 'base/home.html' , context)

def room(request , pk):

    room_details = Room.objects.get(id = pk)
    context = {'room':room_details}        
    return render(request ,"base/room.html" , context)
