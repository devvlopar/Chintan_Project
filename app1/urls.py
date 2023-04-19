from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('vilas/', fun1),
    path('chintan/', chintan),
    path('', f3)
]