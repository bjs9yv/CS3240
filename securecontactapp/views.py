from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ObjectDoesNotExist
from django.core.servers.basehttp import FileWrapper
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, resolve_url
from django.template.response import TemplateResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.static import serve


from .forms import MessageForm, ReportForm, SiteManagerForm, GroupForm, AddUserToGroupForm, FolderForm
from .models import Message, Report, File, Reporter, Folder

import os
import re
from base64 import b64encode, b64decode
from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256

@login_required()
@user_passes_test(lambda u: u.is_active)
def home(request):
    # Display how many messages a user has
    num_messages = len(Message.objects.filter(recipient=request.user))
    return render(request, 'home.html', {'num_messages': num_messages, 'reports': reports})

@login_required()
@user_passes_test(lambda u: u.is_active)
def reports(request):
    # Check user permissions
    can_submit_report = request.user.has_perm('securecontactapp.add_report')
    error = None
    # POST: Process form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request
        form = ReportForm(request.user, request.POST, request.FILES)
        
        # NEW REPORT: If a new report was submitted...
        if 'report' in request.POST:
            # If no permissions...
            if not request.user.has_perm('securecontactapp.add_report'):
                error = 'you do not have permission to submit reports'
            # If valid...
            elif form.is_valid():
                report = form.save()
            # If otherwise invalid...
            else:
                error = 'form not valid'
        
        # DELETE: If the delete button was pressed...
        elif 'delete' in request.POST: 
            # For each checked item...
            for d in request.POST.getlist('del'): 
                r = Report.objects.filter(owner=request.user, id=d) 
                if r.exists():
                    # Delete from database
                    r.get().delete()
        # MOVE TO FOLDER: If the "move to folder" was pressed...
        elif 'move' in request.POST:
            # Get the target folder that the report(s) will be moved to
            folder = Folder.objects.filter(owner=request.user, id=request.POST['folder'])
            if folder.exists():
                folder = folder.get()
            else:
                folder = None
            # For each checked item...
            for d in request.POST.getlist('del'): 
                r = Report.objects.filter(owner=request.user, id=d) 
                if r.exists():
                    # Access report and update its folder, then save it
                    r = r.get()
                    r.folder = folder
                    r.save(update_fields=['folder'])
        elif 'delete_folder' in request.POST:
            folder = Folder.objects.filter(owner=request.user, id=request.POST['folder'])
            if folder.exists():
                folder = folder.get()
                for child in Folder.objects.filter(parent=folder):
                    child.parent = folder.parent
                    child.save(update_fields=['parent'])
                for report in Report.objects.filter(folder=folder):
                    report.folder = folder.parent
                    report.save(update_fields=['folder'])
                folder.delete()
        elif 'rename_folder' in request.POST:
            folder = Folder.objects.filter(owner=request.user, id=request.POST['folder'])
            if folder.exists():
                folder = folder.get()
                folder.name = request.POST['new_name']
                folder.save(update_fields=['name'])
    
    # GET 
    
    form = ReportForm(request.user)
    reports = Report.objects.filter(owner=request.user)
    
    # GET: Filter reports by visibility selector
    if 'visibility' in request.GET:
        reports = reports.filter(private=(request.GET['visibility'] == 'private'))
    
    # GET: Filter reports by folder
    if 'folder' in request.GET:
        folder = Folder.objects.filter(owner=request.user, id=request.GET['folder'])
        if folder.exists():
            reports = reports.filter(folder=folder.get())
        else:
            reports = reports.filter(folder=None)

    reports_and_files = []
    for report in reports:
        files = File.objects.filter(attached_to=report)
        report_hash = SHA256.new(report.description.encode()).hexdigest()
        report = (report,files,report_hash)
        reports_and_files.append(report)
    
    folders = Folder.objects.filter(owner=request.user)
    context = {'form': form, 'reports': reports_and_files, 'folders': folders,
               'error': error, 'can_submit_report': can_submit_report}
    return render(request, 'reports.html', context)

@login_required
@user_passes_test(lambda u: u.is_active)
def edit_report(request, ID):
    report = Report.objects.filter(id=ID)
    if not user_is_site_manager(request.user):
        report = report.filter(owner=request.user)
    if not report.exists() or not request.user.has_perm('securecontactapp.add_report'):
        return HttpResponseRedirect(reverse('reports'))
    error = None

    if request.method == 'POST':
        form = ReportForm(request.user, request.POST, request.FILES, instance=report.get())
        form.save()
        return HttpResponseRedirect(reverse('reports'))

    form = ReportForm(request.user, instance=report.get())
    context = {'form': form, 'error': error}
    return render(request, 'edit_report.html', context)
    
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
    error = None
    if request.method == 'POST':
        if 'create' in request.POST:
            form = GroupForm(data=request.POST)
            if form.is_valid():
                new_group = form.save()
                request.user.groups.add(new_group)
            else:
                error = 'group already exists'
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
    context = {'form': form, 'groups': groups_with_add_form, 'error': error}
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
            permission = Permission.objects.get(codename='add_report')
            usr.user_permissions.add(permission)
            return HttpResponseRedirect(settings.LOGIN_URL)
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

@sensitive_post_parameters('username', 'password')
def get_reports(request):
    if 'username' in request.GET and 'password' in request.GET:
        user = User.objects.filter(username=request.GET['username'])
        if user.exists() and user.get().check_password(request.GET['password']):
            reports = Report.objects.filter(owner=user)
            all_reports = []
            for report in reports:
                report_info_and_files = {}
                report_info_and_files['description'] = report.description
                report_info_and_files['text'] = report.text
                report_info_and_files['files'] = list(map(lambda f: f.file.url, File.objects.filter(attached_to=report)))
                all_reports.append(report_info_and_files)
            return JsonResponse({'reports': all_reports})
    return JsonResponse({})
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
        if 'delete' in request.POST: 
            for d in request.POST.getlist('del'):
                r = Report.objects.filter(id=d)
                r.delete()
                
        form = SiteManagerForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user = User.objects.filter(username=username)
            groupname = form.cleaned_data['group']
            group = Group.objects.filter(name=groupname)
            siteManager = Group.objects.get(name='Site Manager')
            permission = Permission.objects.get(codename='add_report')
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
                    user.user_permissions.remove(permission)
                elif 'resume_reporter' in request.POST:
                    user.user_permissions.add(permission)
                elif group.exists():
                    group = group.get()
                    if 'add_group' in request.POST:
                        user.groups.add(group)
                    elif 'remove_group' in request.POST:
                        user.groups.remove(group)
                user.save()
    else:
        form = SiteManagerForm()
    all_reports = Report.objects.all()
    reports = []
    for report in all_reports:
        files = File.objects.filter(attached_to=report)
        report = (report,files)
        reports.append(report)
    context = {'form': form, 'reports': reports}
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
    # Show group reports
    reports |= Report.objects.filter(group__in=request.user.groups.all())

    if 'q' in request.GET:
        if len(request.GET['q']) >= 2 and request.GET['q'][0] == '/' and request.GET['q'][-1] == '/':
            regex = request.GET['q'][1:-1]
            desc_matches = reports.filter(description__regex=regex)
            text_matches = reports.filter(text__regex=regex)
            keyword_matches = reports.filter(keyword__regex=regex)
            reports = desc_matches | text_matches | keyword_matches
        else:
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
                    reports = desc_matches | text_matches | keyword_matches

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
        form = FolderForm(request.user, request.POST)
        folder = form.save()
    form = FolderForm(request.user)
    context = {'form': form}
    return render(request, 'folder.html', context)

