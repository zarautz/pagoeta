# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('places', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pharmacy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cofg_id', models.PositiveSmallIntegerField(unique=True, verbose_name='label:cofg_id')),
                ('place', models.ForeignKey(related_name='pharmacy', verbose_name='model:Place', to='places.Place')),
            ],
            options={
                'verbose_name': 'model:Pharmacy',
                'verbose_name_plural': 'models:Pharmacies',
            },
        ),
    ]
