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

from .forms import MessageForm, ReportForm
from .models import Message

@login_required()
def home(request):
    return render(request, 'home.html')

@login_required()
def reports(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ReportForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('')
            
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
            _to = form.cleaned_data['message_recipient']
            _from = request.user
            message = form.cleaned_data['message_body']
            # username might not exist
            try:
                sender = User.objects.get(username=_to)
                recipient = _from
                body = message
                message = Message.create(sender,recipient,body)
                #message.save() # NOT WORKING, "column "body" of relation "securecontactapp_message" does not exist"
                return HttpResponse(message.body) # demo purposes only

            except User.DoesNotExist:
                return HttpResponse('no such user')

            # redirect to same page
            return HttpResponseRedirect('')
            
    else:
        form = MessageForm()

        return render(request, 'messages.html', {'form': form})
    
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
