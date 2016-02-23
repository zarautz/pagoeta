# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WeatherCode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=5, verbose_name='label:aemet_code')),
                ('name', models.CharField(max_length=255, verbose_name='label:name')),
                ('name_eu', models.CharField(max_length=255, null=True, verbose_name='label:name')),
                ('name_es', models.CharField(max_length=255, null=True, verbose_name='label:name')),
                ('name_en', models.CharField(max_length=255, null=True, verbose_name='label:name')),
                ('name_fr', models.CharField(max_length=255, null=True, verbose_name='label:name')),
            ],
            options={
                'ordering': ('code',),
                'verbose_name': 'model:WeatherCode',
                'verbose_name_plural': 'models:WeatherCode',
            },
        ),
    ]
