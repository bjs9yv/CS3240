# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('securecontactapp', '0008_auto_20151205_2014'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='group',
        ),
        migrations.AddField(
            model_name='report',
            name='group',
            field=models.ForeignKey(null=True, to='auth.Group', blank=True),
        ),
    ]
