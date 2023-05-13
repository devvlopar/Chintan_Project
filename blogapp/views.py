from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import *
from django.contrib import messages
from django.core.mail import send_mail
import random
from django.conf import settings

# Create your views here.

def index_function(request):
    try:
        u1 = User.objects.get(email = request.session['email'])
        return render(request, 'index.html', {'userdata':u1})
    except:
        return render(request, 'index.html')


def contact(request):
    try:
        u1 = User.objects.get(email = request.session['email'])
        return render(request, 'contact.html', {'userdata':u1})
    except:
        return render(request, 'contact.html')


def beauty(request):
    l1 = Blog.objects.filter(category = 'beauty')
    try:
        u1 = User.objects.get(email = request.session['email'])
        return render(request, 'beauty.html', {'userdata':u1, 'beauty_blogs': l1})
    except:
        return render(request, 'beauty.html', {'beauty_blogs': l1})

def fashion(request):
    l1 = Blog.objects.filter(category = 'fashion')
    try:
        u1 = User.objects.get(email = request.session['email'])
        return render(request, 'fashion.html', {'userdata':u1, 'fashion_blogs': l1})
    except:
        return render(request, 'fashion.html', {'fashion_blogs': l1})


def lifestyle(request):
    l1 = Blog.objects.filter(category = 'lifestyle')

    try:
        u1 = User.objects.get(email = request.session['email'])
        return render(request, 'lifestyle.html', {'userdata':u1, 'lifestyle_blogs': l1})
    except:
        return render(request, 'lifestyle.html', {'lifestyle_blogs': l1})
    

def food(request):
    l1 = Blog.objects.filter(category = 'food')

    try:
        u1 = User.objects.get(email = request.session['email'])
        return render(request, 'food.html', {'userdata':u1, 'food_blogs': l1})
    except:
        return render(request, 'food.html', {'food_blogs': l1})


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
        

def login(request):
    if request.method == 'POST':
        try:
            u1 = User.objects.get(email = request.POST['email'])
            if u1.password == request.POST['password']:
                request.session['email'] = request.POST['email'] #iss line se login ho gaya hai
                return render(request, 'index.html', {'userdata': u1})
            else:
                return render(request, 'login.html', {'hemlata': 'Invalid Password'})
        except:
            #agar error aaya hai matalab email invalid hai, account  hi nahi hai
            return render(request, 'login.html', {'hemlata': 'Email Does Not Exist!'})

    else:
        return render(request, 'login.html')
    

def logout(request):
    del request.session['email']
    return redirect('index')


def add_blog(request):
    b_form = BlogForm()
    try:
        u1 = User.objects.get(email = request.session['email'])
        if request.method == 'GET':
            return render(request, 'add_blog.html', {'form': b_form, 'userdata': u1})
        else:
            #blog hai wo db mein entry karwana hai
            # template pe se data request.POST naam ki dictionary mein aata hai
            Blog.objects.create(
                title = request.POST['title'], 
                des = request.POST['des'],
                pic = request.FILES['pic'],
                user = u1, #user variable pe FOREIGNKEY field liya hai isiliye User ka obj dena hai
                category = request.POST['category']
            )
            return render(request, 'add_blog.html', {'form': b_form, 'userdata':u1, 'msg': 'Successfully Created'})
    except:
        return redirect('login')

def my_blogs(request):
    try:
        #u1 wo user hai jisne currently login karke rakha hai
        u1 = User.objects.get(email = request.session['email'])
        l1 = Blog.objects.filter(user = u1)
        return render(request, 'my_blogs.html', {'userdata':u1, 'user_blogs': l1})
    except:
        return redirect('login')