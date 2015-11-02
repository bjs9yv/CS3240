from django.db import models

class User(models.Model):
    group = models.ForeignKey('UserGroup')

class UserGroup(models.Model):
    pass

class Report(models.Model):
    owner = models.ForeignKey('User')
    folder = models.ForeignKey('Folder')

class Folder(models.Model):
    parent = models.ForeignKey('Folder')

class File(models.Model):
    attached_to = models.ForeignKey('Report')

class Message(models.Model):
    sender = models.ForeignKey('User', related_name='message_sender')
    recipient = models.ForeignKey('User', related_name='message_recipient')
