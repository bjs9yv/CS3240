# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('securecontactapp', '0003_auto_20151116_1353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='folder',
            field=models.ForeignKey(blank=True, to='securecontactapp.Folder', null=True),
        ),
    ]
