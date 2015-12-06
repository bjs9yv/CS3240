# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0006_require_contenttypes_0002'),
        ('securecontactapp', '0003_auto_20151130_1702'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reportergroup',
            name='owner',
        ),
        migrations.AddField(
            model_name='folder',
            name='name',
            field=models.CharField(default='NoGroups', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='folder',
            name='owner',
            field=models.ForeignKey(default='None', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='report',
            name='group',
            field=models.ManyToManyField(to='auth.Group'),
        ),
        migrations.AlterField(
            model_name='folder',
            name='parent',
            field=models.ForeignKey(blank=True, to='securecontactapp.Folder', null=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='keyword',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='ReporterGroup',
        ),
    ]
