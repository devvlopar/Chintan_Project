from django.shortcuts import render
from django.http import HttpResponse
from .forms import *

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
    if request.method == 'GET':
        f_obj = UserForm()
        return render(request, 'register.html', {'form': f_obj})
    else:
        # print(request.POST)
        d_obj = UserForm(request.POST)
        if d_obj.is_valid():
            d_obj.save()
            return HttpResponse('SUCCESS')
        else:
            return HttpResponse('dtata')