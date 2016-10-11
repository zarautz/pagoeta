# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0002_xeroximage_created_at'),
    ]

    operations = [
        migrations.DeleteModel(
            name='XeroxImage',
        ),
    ]
