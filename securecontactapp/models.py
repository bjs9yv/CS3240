from django.db import models
from django.contrib.auth.models import User

# User-submitted Reports
class Report(models.Model):
    owner = models.ForeignKey(User)
    folder = models.ForeignKey('Folder', blank=True, null=True)
    private = models.BooleanField(default=False)
    text = models.TextField()
    timestamp = models.TimeField(auto_now_add=True)
    # TODO: NEED TO ADD SHORT DESCRIPTION IN ADDITION TO LONG DESCRIPTION
    # TODO: CONSIDER ADDING LOCATION 
    # TODO: CONSIDER ADDING TAGS OR KEYWORDS

# Folders to hold other Reports
class Folder(models.Model):
    parent = models.ForeignKey('Folder')

# helper function to give path to upload files to
def report_filename(instance, filename):
    return instance.attached_to.owner.username + '/' + filename

# Uploaded files attached to Reports
class File(models.Model):
    attached_to = models.ForeignKey('Report')
    encrypted = models.BooleanField(default=False)
    file = models.FileField(upload_to=report_filename)
    timestamp = models.TimeField(auto_now_add=True)

# Message sent from one user to another
class Message(models.Model):
    sender = models.ForeignKey(User, related_name='message_sender')
    recipient = models.ForeignKey(User, related_name='message_recipient')
    body = models.TextField()
    timestamp = models.TimeField(auto_now_add=True)
    opened = models.BooleanField(default=False)
    encrypted = models.BooleanField(default=False)

class Reporter(models.Model):
    user = models.OneToOneField(User)
    publickey = models.TextField()
    privatekey = models.TextField()

class ReporterGroup(models.Model):
    # NOTE: ACCORDING TO SPECS, GROUP NAMES SHOULD BE UNIQUE
    name = models.TextField()
    owner = models.ForeignKey(User)
    # group = models.ForeignKey(Group)
    is_hidden = models.BooleanField()
    members_can_invite = models.BooleanField()
