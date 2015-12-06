# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('securecontactapp', '0004_auto_20151205_1806'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='group',
            field=models.ManyToManyField(to='auth.Group', blank=True),
        ),
    ]
