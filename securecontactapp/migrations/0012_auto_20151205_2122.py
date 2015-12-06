# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('securecontactapp', '0011_auto_20151205_2122'),
    ]

    operations = [
        migrations.RenameField(
            model_name='report',
            old_name='share_group',
            new_name='group',
        ),
    ]
