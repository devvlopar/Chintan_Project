from django.contrib import admin
from django.urls import path, include
from blogapp.views import *

urlpatterns = [
    path('', index_function, name='index'),
    path('contact/', contact, name='qwerty'), #for your example
    path('beauty/', beauty, name='beauty'),
    path('fashion/', fashion, name='fashion'),
    path('register/', register, name='register'),
    path('otp/', otp, name='otp'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('add_blog/', add_blog, name='add_blog'),
    path('my_blogs/', my_blogs, name='my_blogs'),








]