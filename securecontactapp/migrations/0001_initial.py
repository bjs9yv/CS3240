# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import securecontactapp.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('encrypted', models.BooleanField(default=False)),
                ('file', models.FileField(upload_to=securecontactapp.models.report_filename)),
                ('timestamp', models.TimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(null=True, blank=True, to='securecontactapp.Folder')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('body', models.TextField()),
                ('timestamp', models.TimeField(auto_now_add=True)),
                ('opened', models.BooleanField(default=False)),
                ('encrypted', models.BooleanField(default=False)),
                ('recipient', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='message_recipient')),
                ('sender', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='message_sender')),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('private', models.BooleanField(default=False)),
                ('encrypted', models.BooleanField(default=False)),
                ('description', models.TextField()),
                ('keyword', models.TextField(null=True, blank=True)),
                ('text', models.TextField()),
                ('timestamp', models.TimeField(auto_now=True)),
                ('datestamp', models.DateField(auto_now=True)),
                ('folder', models.ForeignKey(null=True, blank=True, to='securecontactapp.Folder')),
                ('group', models.ManyToManyField(to='auth.Group', blank=True)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Reporter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('publickey', models.TextField()),
                ('privatekey', models.TextField()),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='file',
            name='attached_to',
            field=models.ForeignKey(to='securecontactapp.Report'),
        ),
    ]
