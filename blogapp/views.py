from django.shortcuts import render
from django.http import HttpResponse
from .forms import *
from django.contrib import messages
from django.core.mail import send_mail
import random
from django.conf import settings

# Create your views here.

def index_function(request):
    return render(request, 'index.html')


def contact(request):
    return render(request, 'contact.html')

def beauty(request):
    return render(request, 'beauty.html')

def fashion(request):
    return render(request, 'fashion.html')


def register(request):
    f_obj = UserForm()
    if request.method == 'GET':
        return render(request, 'register.html', {'form': f_obj})
    else:
        try:
            u1 = User.objects.get(email = request.POST['email'])
            return render(request , 'register.html', {'msg': 'Email already Exists', 'form': f_obj})
        except:
            try:
                User.objects.get(username = request.POST['username'])
                return render(request , 'register.html', {'msg': 'Username already Exists', 'form': f_obj})
            except:   
                global c_otp
                c_otp = random.randint(100000,999999)
                subject = "Email Verify"
                message = f"Hello!!\nYour OTP is {c_otp}"
                from_em = settings.EMAIL_HOST_USER
                rec = [request.POST['email']]
                send_mail(subject, message, from_em, rec)
                global user_data
                user_data = [
                    request.POST['first_name'],
                    request.POST['last_name'],
                    request.POST['email'],
                    request.POST['username'],
                    request.POST['password']]
                return render(request, 'otp.html')

        
        
def otp(request):
    f_obj = UserForm()
    if int(request.POST['u_otp']) == c_otp:
        User.objects.create(
            first_name = user_data[0],
            last_name = user_data[1],
            email = user_data[2],
            username = user_data[3],
            password = user_data[4]
        )
        return render(request, 'register.html', {'form': f_obj, 'msg': 'Successfully created!!'})
    else:
        return render(request, 'otp.html', {'msg': 'Wrong OTP, Enter again'})
        



        
        