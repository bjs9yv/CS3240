from django.db import models
from django.contrib.auth.models import User, Group

# User-submitted Reports
class Report(models.Model):
    owner = models.ForeignKey(User)
    folder = models.ForeignKey('Folder', blank=True, null=True)
    private = models.BooleanField(default=False)
    encrypted = models.BooleanField(default=False)
    description = models.TextField()
    keyword = models.TextField(null=True, blank=True)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)
    group = models.ManyToManyField(Group, blank=True)
    
# Folders to hold other Reports
class Folder(models.Model):
    owner = models.ForeignKey(User)
    parent = models.ForeignKey('Folder', blank=True, null=True)
    name = models.CharField(max_length=20)
    
    def __str__(self):
        if self.parent:
            parent = str(self.parent)
        else:
            parent = '/'
        return parent + self.name + '/'

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
