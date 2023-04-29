from django.contrib import admin
from django.urls import path, include
from blogapp.views import *

urlpatterns = [
    path('', index_function, name='index'),
    path('contact/', contact, name='contact')
]