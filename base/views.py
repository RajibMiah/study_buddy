from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def home(request):
    return HttpResponse('this is home')

def room(request):
    return HttpResponse('this is room')
