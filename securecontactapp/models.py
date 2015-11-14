from django.db import models
from django.contrib.auth.models import User

# User-submitted Reports
class Report(models.Model):
    owner = models.ForeignKey(User)
    folder = models.ForeignKey('Folder')

# Folders to hold other Reports
class Folder(models.Model):
    parent = models.ForeignKey('Folder')

# Uploaded files attached to Reports
class File(models.Model):
    attached_to = models.ForeignKey('Report')

# Message sent from one user to another
class Message(models.Model):
    sender = models.ForeignKey(User, related_name='message_sender')
    recipient = models.ForeignKey(User, related_name='message_recipient')
    body = models.TextField()
    timestamp = models.TimeField(auto_now_add=True)
    opened = models.BooleanField(default=False)