from django.contrib import admin
from django.urls import path, include
from blogapp.views import *

urlpatterns = [
    path('', index_function, name='index'),
    path('contact/', contact, name='qwerty'), #for your example
    path('beauty/', beauty, name='beauty'),
    path('fashion/', fashion, name='fashion'),
    path('register/', register, name='register'),



]