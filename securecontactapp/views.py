from django.conf import settings
from django.shortcuts import render, resolve_url
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django.template.response import TemplateResponse
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.db.models.signals import post_save

from .forms import MessageForm, ReportForm, SiteManagerForm
from .models import Message, Report, File, Reporter

import os
from Crypto import Random
from Crypto.PublicKey import RSA

@login_required()
def home(request):
    return render(request, 'home.html')

@login_required()
def reports(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ReportForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            # TODO: process the data in form.cleaned_data as required
            text = form.cleaned_data['report_body']
            r = Report(owner=request.user, text=text)
            r.save()
            for fn in request.FILES:
                f = File(file=request.FILES[fn], attached_to=r)
                f.save()
            # redirect to a new URL:
            return HttpResponseRedirect('')
        else:
            return HttpResponse('nope')
            
    else:
        form = ReportForm()

        return render(request, 'reports.html', {'form': form})
    
    
@login_required
def messages(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = MessageForm(request.POST)
        if 'message' in request.POST:
            
            # check whether it's valid:
            if form.is_valid():
                # extract data from form.cleaned_data 
                to = form.cleaned_data['message_recipient']
                sender = request.user
                body = form.cleaned_data['message_body']
                e = form.cleaned_data['encrypted']
                # recipient username might not exist
                user = User.objects.filter(username=to)
                if user.exists():
                    if e:
                        u = User.objects.get(username=to)
                        public_key = RSA.importKey(u.reporter.publickey)
                        enc_data = public_key.encrypt(body.encode(),48)
                        body = enc_data
                    m = Message(sender=sender, recipient=user.get(), body=body, encrypted=e)
                    m.save()
            # redirect to same page
            return HttpResponseRedirect('')
        elif 'delete' in request.POST: 
            for d in request.POST.getlist('del'): 
                m = Message.objects.get(id=d) 
                m.delete()
        elif 'decrypt' in request.POST:
            u = User.objects.get(username=request.user)
            private_key = RSA.importKey(u.reporter.privatekey)
            #m = Message.objects.get(id=ID FROM REQUEST CHECKBOX)
    else:
        form = MessageForm()

    messages = Message.objects.filter(recipient=request.user)
    return render(request, 'messages.html', {'form': form, 'messages': messages})
    
@login_required()
def groups(request):
    return render(request, 'groups.html')

@login_required()
def account(request):
    if request.method == "POST":
        # generate keypair
        g = Random.new().read
        key = RSA.generate(2048, g)
        private = key.exportKey(format="PEM")
        public = key.publickey().exportKey(format="PEM")
        # make a Reporter object
        usr = User.objects.get(username=request.user)
        reporter = Reporter(user=usr,publickey=public,privatekey=private)
        reporter.save()
        # TODO prevent user from pressing the button again, make button go away? 
    return render(request, 'account.html')

@sensitive_post_parameters('username', 'password1', 'password2')
@csrf_protect
@never_cache
def registration(request):
    if request.method == "POST":
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(resolve_url(settings.LOGIN_URL))
    else:
        form = UserCreationForm()

    context = {'form': form}
    return TemplateResponse(request, 'registration/registration.html', context)

@sensitive_post_parameters('username', 'password')
def check_login(request):
    valid = False
    if 'username' in request.GET and 'password' in request.GET:
        user = User.objects.filter(username=request.GET['username'])
        if user.exists():
            valid = user.get().check_password(request.GET['password'])
    elif 'username' in request.POST and 'password' in request.POST:
        user = User.objects.filter(username=request.POST['username'])
        if user.exists():
            valid = user.get().check_password(request.POST['password'])

    return JsonResponse({'valid': valid})

@login_required
def humans(request):
    with open('/app/team16project/static/humans.txt', 'r') as f:
        return HttpResponse(f.read())

def user_is_site_manager(user):
    return user.groups.filter(name='Site Manager').exists()

@user_passes_test(user_is_site_manager)
@csrf_protect
def site_manager(request):
    if request.method == 'POST':
        form = SiteManagerForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user = User.objects.filter(username=username)
            siteManager = Group.objects.get(name='Site Manager')
            if user.exists():
                user = user.get()
                if 'promote' in request.POST:
                    user.groups.add(siteManager)
                elif 'demote' in request.POST:
                    user.groups.remove(siteManager)
                elif 'suspend_access' in request.POST:
                    user.is_active = False
                elif 'resume_access' in request.POST:
                    user.is_active = True
                elif 'suspend_reporter' in request.POST:
                    user.user_permissions.remove('securecontactapp.add_report')
                elif 'resume_reporter' in request.POST:
                    user.user_permissions.add('securecontactapp.add_report')
                user.save()
    else:
        form = SiteManagerForm()
    context = {'form': form}
    return render(request, 'sitemanager.html', context)
