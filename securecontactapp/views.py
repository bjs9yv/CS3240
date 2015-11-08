from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url = '/login')
def home(request):
    return HttpResponse('Hello there!')

def registration(request):
    return HttpResponse('lets make a new account')
