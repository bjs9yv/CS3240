from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url = '/login')
def home(request):
    return HttpResponse('Hello there!')

#@csrf_protect # protects against cross site request forgeries
def registration(request):
    # create a new user here with magic
    return HttpResponse('lets make a new account')
