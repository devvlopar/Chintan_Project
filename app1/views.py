from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def fun1(request):
    return HttpResponse("Hi I am Master in Computer Application")

# python manage.py startapp app_name

def chintan(request):
    return HttpResponse("this is chintan")

def f3(request):
    return HttpResponse('hey')