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
    path('food/', food, name='food'),
    path('lifestyle/', lifestyle, name='lifestyle'),
    path('single_blog/<int:bid>', single_blog, name='single_blog'),
    path('add_comment/<int:pk>', add_comment, name='add_comment'),
    path('donate/<int:bid>', donate, name='donate'),
    path('pay_init/', pay_init, name='pay_init'),
    path('pay_init/paymenthandler/', paymenthandler, name='paymenthandler'),
    path('search/', search, name='search'),
    path('delete_blog/<int:bpk>', delete_blog, name='delete_blog'),




    
]