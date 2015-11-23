# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('securecontactapp', '0004_auto_20151116_1632'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='encrypted',
            field=models.BooleanField(default=False),
        ),
    ]
