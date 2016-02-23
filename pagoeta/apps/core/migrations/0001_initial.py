# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='XeroxImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hash', models.CharField(unique=True, max_length=40)),
                ('url', models.URLField(null=True, blank=True)),
            ],
            options={
                'db_table': 'core_xerox_image',
            },
        ),
    ]
