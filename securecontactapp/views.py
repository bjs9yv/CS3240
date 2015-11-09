from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


# Create your views here.
@login_required(login_url = '/login')
def home(request):
    return HttpResponse('Hello there!')

@sensitive_post_parameters()
@csrf_protect
@never_cache
def registration(request,template_name='registration/registration.html'):
    # get user form data here with magic...
    # maybe by modifying this: https://docs.djangoproject.com/en/1.8/_modules/django/contrib/auth/views/

    # create a new user here with the following:
    # user = User.objects.create_user('john', 'lennon@thebeatles.com', 'pass')

    return render(request, template_name)
