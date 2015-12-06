# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('securecontactapp', '0002_auto_20151130_1654'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
