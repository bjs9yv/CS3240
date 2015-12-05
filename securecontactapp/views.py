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

from .forms import MessageForm, ReportForm, SiteManagerForm, GroupForm, AddUserToGroupForm, FolderForm
from .models import Message, Report, File, Reporter, Folder

import os
from base64 import b64encode, b64decode
from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

@login_required()
@user_passes_test(lambda u: u.is_active)
def home(request):
    # display how many messages a user has
    num_messages = len(Message.objects.filter(recipient=request.user))
    return render(request, 'home.html', {'num_messages': num_messages, 'reports': reports})

@login_required()
@user_passes_test(lambda u: u.is_active)
def reports(request):
    reports = Report.objects.filter(owner=request.user)
    can_submit_report = request.user.has_perm('securecontactapp.add_report')
    error = None
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ReportForm(request.POST, request.FILES)
        if 'report' in request.POST:
            # check whether it's valid:
            if not request.user.has_perm('securecontactapp.add_report'):
                error = 'you do not have permission to submit reports'
            elif form.is_valid():
                report = form.save(commit=False)
                report.owner = request.user
                if report.folder != None and report.folder.owner != request.user:
                    report.folder = None
                # TODO: if encrypted == True... encrypt the file(s) in a similar manner to how message encryption was done below
                report.save()
                for fn in request.FILES:
                    f = File(file=request.FILES[fn], attached_to=report)
                    f.save()
            else:
                error = 'form not valid'
        elif 'delete' in request.POST: 
            for d in request.POST.getlist('del'): 
                r = Report.objects.filter(owner=request.user, id=d) 
                if r.exists():
                    r.get().delete()
        elif 'move_to_folder' in request.POST:
            folder = Folder.objects.filter(owner=request.user, id=request.POST['move_to_folder'])
            if folder.exists():
                folder = folder.get()
            else:
                folder = None
            for d in request.POST.getlist('del'): 
                r = Report.objects.filter(owner=request.user, id=d) 
                if r.exists():
                    r = r.get()
                    r.folder = folder
                    r.save(update_fields=['folder'])
    else:
        form = ReportForm()
    form.fields['folder'].queryset = Folder.objects.filter(owner=request.user)

    reports = Report.objects.filter(owner=request.user)
    
    if 'visibility' in request.GET:
        reports = reports.filter(private=(request.GET['visibility'] == 'private'))
    if 'folder' in request.GET:
        folder = Folder.objects.filter(owner=request.user, id=request.GET['folder'])
        if folder.exists():
            reports = reports.filter(folder=folder.get())
        else:
            reports = reports.filter(folder=None)

    reports_and_files = []
    for report in reports:
        files = File.objects.filter(attached_to=report)
        report = (report,files)
        reports_and_files.append(report)
    folders = Folder.objects.filter(owner=request.user)
    context = {'form': form, 'reports': reports_and_files, 'folders': folders,
            'error': error, 'can_submit_report': can_submit_report}
    return render(request, 'reports.html', context)
    
@login_required
@user_passes_test(lambda u: u.is_active)
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
                        cipher = PKCS1_OAEP.new(public_key)
                        enc_data = b64encode(cipher.encrypt(body.encode('UTF-8')))
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
            for d in request.POST.getlist('del'): 
                cipher = PKCS1_OAEP.new(private_key)
                m = Message.objects.get(id=d)
                try:
                    m.body = cipher.decrypt(b64decode(m.body)).decode(encoding='UTF-8')
                except:
                    # if invalid ciphertext blob
                    continue
                m.save()
    else:
        form = MessageForm()

    messages = Message.objects.filter(recipient=request.user)
    return render(request, 'messages.html', {'form': form, 'messages': messages})
    
@login_required()
@user_passes_test(lambda u: u.is_active)
def groups(request):
    if request.method == 'POST':
        if 'create' in request.POST:
            form = GroupForm(data=request.POST)
            if form.is_valid():
                new_group = form.save()
                # TODO: group names are unique
                #if Group.objects.get(name=new_group.name):
                   # return HttpResponse('Group already exists')
                request.user.groups.add(new_group)
            else:
                return HttpResponse('Group already exists')
        else:
            for key in request.POST.keys():
                if key.startswith('add '):
                    form = AddUserToGroupForm(data=request.POST)
                    group = Group.objects.get(name=key[4:])
                    user = User.objects.filter(username=request.POST['username'])
                    if request.user in group.user_set.all() and user.exists():
                        group.user_set.add(user.get())
    form = GroupForm()
    groups = request.user.groups.all()
    groups_with_add_form = map(lambda g: (g, AddUserToGroupForm(), g.user_set.all()), groups)
    context = {'form': form, 'groups': groups_with_add_form}
    return render(request, 'groups.html', context)

@login_required()
@user_passes_test(lambda u: u.is_active)
def account(request):
    context = {'site_manager': user_is_site_manager(request.user)}
    return render(request, 'account.html', context)

@sensitive_post_parameters('username', 'password1', 'password2')
@csrf_protect
@never_cache
def registration(request):
    if request.method == "POST":
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            usr = form.save()
            # In addition to creating an account we will also generate keypair
            g = Random.new().read
            key = RSA.generate(2048, g)
            private = key.exportKey(format="PEM")
            public = key.publickey().exportKey(format="PEM")
            # And make a Reporter object that adds data to our User object
            reporter = Reporter(user=usr,publickey=public,privatekey=private)
            reporter.save()
            usr.user_permissions.add('securecontactapp.add_report')
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

def humans(request):
    with open('/app/team16project/static/humans.txt', 'r') as f:
        return HttpResponse(f.read())

def user_is_site_manager(user):
    return user.groups.filter(name='Site Manager').exists()

@user_passes_test(user_is_site_manager)
@user_passes_test(lambda u: u.is_active)
@csrf_protect
def site_manager(request):
    if request.method == 'POST':
        form = SiteManagerForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user = User.objects.filter(username=username)
            groupname = form.cleaned_data['group']
            group = Group.objects.filter(name=groupname)
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
                elif group.exists():
                    group = group.get()
                    if 'add_group' in request.POST:
                        user.groups.add(group)
                    elif 'remove_group' in request.POST:
                        user.groups.remove(group)
                user.save()
    else:
        form = SiteManagerForm()
    context = {'form': form}
    return render(request, 'sitemanager.html', context)

@login_required()
@user_passes_test(lambda u: u.is_active)
def search(request):
    reports = Report.objects.all()
    # Only show public reports, unless user is SM
    if not user_is_site_manager(request.user):
        reports = reports.filter(private=False)
    # But show user's own private reports
    reports |= Report.objects.filter(owner=request.user)

    if 'q' in request.GET:
        for term in request.GET['q'].split():
            if term[0] == '-':
                regex = r'\y%s\y' % term[1:]
                desc_matches = reports.exclude(description__iregex=regex)
                text_matches = reports.exclude(text__iregex=regex)
                keyword_matches = reports.exclude(keyword__iregex=regex)
                reports = desc_matches & text_matches & keyword_matches
            else:
                regex = r'\y%s\y' % term
                desc_matches = reports.filter(description__iregex=regex)
                text_matches = reports.filter(text__iregex=regex)
                keyword_matches = reports.filter(keyword__iregex=regex)
                reports = desc_matches | text_matches & keyword_matches

    reports_and_files = []
    for report in reports:
        files = File.objects.filter(attached_to=report)
        report = (report,files)
        reports_and_files.append(report)
    context = {'reports': reports_and_files}
    return render(request, 'search.html', context)

@login_required()
@user_passes_test(lambda u: u.is_active)
def folder(request):
    if request.method == 'POST':
        form = FolderForm(request.POST)
        folder = form.save(commit=False)
        folder.owner = request.user
        folder.save()
    else:
        form = FolderForm()
    form.fields['parent'].queryset = Folder.objects.filter(owner=request.user)
    context = {'form': form}
    return render(request, 'folder.html', context)
