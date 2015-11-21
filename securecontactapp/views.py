from django.conf import settings
from django.shortcuts import render, resolve_url
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.template.response import TemplateResponse
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.db.models.signals import post_save

from .forms import MessageForm, ReportForm
from .models import Message, Report, File

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
        # check whether it's valid:
        if form.is_valid():
            # extract data from form.cleaned_data 
            to = form.cleaned_data['message_recipient']
            sender = request.user
            body = form.cleaned_data['message_body']
            # recipient username might not exist
            user = User.objects.filter(username=to)
            if user.exists():
                m = Message(sender=sender, recipient=user.get(), body=body)
                m.save()
        # redirect to same page
        return HttpResponseRedirect('')
            
    else:
        form = MessageForm()
        messages = Message.objects.filter(recipient=request.user, opened=False)
        return render(request, 'messages.html', {'form': form, 'messages': messages})
    
@login_required()
def groups(request):
    return render(request, 'groups.html')

@login_required()
def account(request):
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
    return HttpResponse(os.getcwd() + 'team16project/static/humans.txt')
    with open(os.getcwd() + 'team16project/static/humans.txt', 'r') as f:
        return HttpResponse(f.read())
