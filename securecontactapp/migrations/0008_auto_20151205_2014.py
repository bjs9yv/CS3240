# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('securecontactapp', '0007_auto_20151205_1957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='group',
            field=models.ManyToManyField(default='No Group', to='auth.Group'),
        ),
    ]
