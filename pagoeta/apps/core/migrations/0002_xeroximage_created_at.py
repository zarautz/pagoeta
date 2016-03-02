# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='xeroximage',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 2, 16, 5, 54, 653349, tzinfo=utc),
                                       auto_now_add=True),
            preserve_default=False,
        ),
    ]
