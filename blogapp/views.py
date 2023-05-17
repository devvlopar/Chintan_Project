from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import *
from django.contrib import messages
from django.core.mail import send_mail
import random
from django.conf import settings
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
# Create your views here.

razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


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


def single_blog(request, bid):
    #bid blog ki id jo hume page pe show karwana hai
    b1 = Blog.objects.get(id = bid)
    f_list = Comment.objects.filter(blog = b1)
    try:
        u1 = User.objects.get(email = request.session['email'])
        d_list = Donate.objects.filter(blog = b1)
        total_doantions = 0
        for i in d_list:
            total_doantions += i.amount

        return render(request, 'single_blog.html', {'userdata':u1, 'blog_data': b1, 'f_comments':f_list, 't_amount': total_doantions})
    except:
        return render(request, 'single_blog.html', {'blog_data': b1, 'f_comments': f_list, 't_amount': total_doantions})
    

def add_comment(request, pk): #pk mein wo blog ka id aa rha hai
    try:
        u1 = User.objects.get(email = request.session['email'])
        b1 = Blog.objects.get(id = pk)
        Comment.objects.create(
            message = request.POST['troll'],
            user = u1, #yahan pe foreign key field hone ki wajah se OBJ diya
            blog = b1
            )
        f_list = Comment.objects.filter(blog = b1)
        return render(request, 'single_blog.html', {'userdata':u1, 'blog_data': b1, 'f_comments':f_list})
    except:
        return redirect('login')
    

def donate(request, bid):
    try:
        u1 = User.objects.get(email = request.session['email'])
        global b1
        b1 = Blog.objects.get(id = bid)
        return render(request, 'donate.html', {'userdata':u1, 'blogdata': b1})
    except:
        return redirect('login')
    



#--------------COPIED CODE PAYMENT------------------#

def pay_init(request):
    global amount_rupee
    amount_rupee = int(request.POST['pamount'])
    currency = 'INR'
    amount = amount_rupee * 100 # Rs. 200
 
    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))
 
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'
 
    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
 
    return render(request, 'payment.html', context=context)
 


@csrf_exempt
def paymenthandler(request):
 
    # only accept POST request.
    if request.method == "POST":
        try:
           
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is not None:
                amount = amount_rupee * 100  # Rs. 200
                try:
 
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
                    u1 = User.objects.get(email = request.session['email'])
                    Donate.objects.create(
                        user = u1,
                        blog = b1,
                        amount = amount_rupee
                    )
                    # render success page on successful caputre of payment
                    return render(request, 'success.html')
                except:
 
                    # if there is an error while capturing payment.
                    return render(request, 'fail.html')
            else:
 
                # if signature verification fails.
                return render(request, 'fail.html')
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()
    

def search(request):
    word = request.GET['search']
    # ye niche wali line pe hum username ke hisaab se blogs filter kar rhe hai
    # f_list = Blog.objects.filter(user_username__icontains = word)

    f_list = Blog.objects.filter(title__icontains = word)
    try:
        u1 = User.objects.get(email = request.session['email'])
        return render(request, 'search.html', {'userdata':u1, 'blogs': f_list})
    except:
        return render(request, 'search.html', {'blogs' : f_list})

def delete_blog(request, bpk):
    b_obj = Blog.objects.get(id = bpk)
    b_obj.delete() # ye wala blog database mein se delete ho jaayega
    return redirect('my_blogs')
