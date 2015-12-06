# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('securecontactapp', '0005_auto_20151205_1819'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='group',
        ),
        migrations.AddField(
            model_name='report',
            name='group',
            field=models.ForeignKey(blank=True, null=True, to='auth.Group'),
        ),
    ]
