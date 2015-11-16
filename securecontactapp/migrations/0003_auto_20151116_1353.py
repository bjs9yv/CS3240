# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc
import securecontactapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('securecontactapp', '0002_auto_20151109_2233'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='encrypted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='file',
            name='file',
            field=models.FileField(default=b'', upload_to=securecontactapp.models.report_filename),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='file',
            name='timestamp',
            field=models.TimeField(default=datetime.datetime(2015, 11, 16, 19, 52, 51, 539066, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='message',
            name='body',
            field=models.TextField(default=b''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='message',
            name='opened',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='message',
            name='timestamp',
            field=models.TimeField(default=datetime.datetime(2015, 11, 16, 19, 53, 5, 328498, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='report',
            name='private',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='report',
            name='text',
            field=models.TextField(default=b''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='report',
            name='timestamp',
            field=models.TimeField(default=datetime.datetime(2015, 11, 16, 19, 53, 19, 628284, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
