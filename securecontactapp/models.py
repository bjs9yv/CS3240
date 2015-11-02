from django.db import models

class UserGroup(models.Model):
    pass

class User(models.Model):
    group = models.ForeignKey(UserGroup)

class Report(models.Model):
    owner = models.ForeignKey(User)
    folder = models.ForeignKey(Folder)

class File(models.Model):
    attached_to = models.ForeignKey(Report)

class Message(models.Model):
    sender = models.ForeignKey(User)
    recipient = models.ForeignKey(User)

class Folder(models.Model):
    parent = models.ForeignKey(Folder)
