# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import securecontactapp.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('encrypted', models.BooleanField(default=False)),
                ('file', models.FileField(upload_to=securecontactapp.models.report_filename)),
                ('timestamp', models.TimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('parent', models.ForeignKey(to='securecontactapp.Folder')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
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
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('private', models.BooleanField(default=False)),
                ('encrypted', models.BooleanField(default=False)),
                ('description', models.TextField()),
                ('keyword', models.TextField(null=True)),
                ('text', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('folder', models.ForeignKey(null=True, to='securecontactapp.Folder', blank=True)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Reporter',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('publickey', models.TextField()),
                ('privatekey', models.TextField()),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ReporterGroup',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.TextField()),
                ('is_hidden', models.BooleanField()),
                ('members_can_invite', models.BooleanField()),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='file',
            name='attached_to',
            field=models.ForeignKey(to='securecontactapp.Report'),
        ),
    ]
