# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import imagekit.models.fields
import pagoeta.apps.core.models


class Migration(migrations.Migration):
    dependencies = [
        ('places', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=100, verbose_name='label:code', db_index=True)),
                ('name', models.CharField(max_length=255, verbose_name='label:name')),
                ('name_eu', models.CharField(max_length=255, null=True, verbose_name='label:name')),
                ('name_es', models.CharField(max_length=255, null=True, verbose_name='label:name')),
                ('name_en', models.CharField(max_length=255, null=True, verbose_name='label:name')),
                ('name_fr', models.CharField(max_length=255, null=True, verbose_name='label:name')),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'model:Category',
                'verbose_name_plural': 'models:Category',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='label:name')),
                ('name_eu', models.CharField(max_length=255, null=True, verbose_name='label:name')),
                ('name_es', models.CharField(max_length=255, null=True, verbose_name='label:name')),
                ('name_en', models.CharField(max_length=255, null=True, verbose_name='label:name')),
                ('name_fr', models.CharField(max_length=255, null=True, verbose_name='label:name')),
                ('description', models.TextField(verbose_name='label:description')),
                ('description_eu', models.TextField(null=True, verbose_name='label:description')),
                ('description_es', models.TextField(null=True, verbose_name='label:description')),
                ('description_en', models.TextField(null=True, verbose_name='label:description')),
                ('description_fr', models.TextField(null=True, verbose_name='label:description')),
                ('start_date', models.DateField(verbose_name='label:start_date')),
                ('end_date', models.DateField(null=True, verbose_name='label:end_date', blank=True)),
                ('start_time', models.TimeField(null=True, verbose_name='label:start_time', blank=True)),
                ('end_time', models.TimeField(help_text='help_text:end_time', null=True, verbose_name='label:end_time',
                                              blank=True)),
                ('afternoon_start_time', models.TimeField(null=True, verbose_name='label:afternoon_start_time',
                                                          blank=True)),
                ('afternoon_end_time', models.TimeField(help_text='help_text:afternoon_end_time', null=True,
                                                        verbose_name='label:afternoon_end_time', blank=True)),
                ('is_all_day_event', models.BooleanField(default=False, help_text='help_text:is_all_day_event',
                                                         verbose_name='label:is_all_day_event')),
                ('price', models.DecimalField(null=True, verbose_name='label:price', max_digits=6, decimal_places=2,
                                              blank=True)),
                ('url', models.URLField(null=True, verbose_name='label:url', blank=True)),
                ('is_featured', models.BooleanField(default=False, verbose_name='label:is_featured')),
                ('is_superevent', models.BooleanField(default=False, help_text='help_text:is_superevent',
                                                      verbose_name='label:is_superevent')),
                ('is_visible', models.BooleanField(default=True, verbose_name='label:is_visible')),
                ('category', models.ForeignKey(related_name='events', verbose_name='model:Category',
                                               to='events.Category')),
                ('parent', models.ForeignKey(related_name='subevents', blank=True, to='events.Event',
                                             help_text='help_text:parent_superevent', null=True,
                                             verbose_name='label:parent_superevent')),
                ('place', models.ForeignKey(related_name='events', verbose_name='model:Place', blank=True,
                                            to='places.Place', null=True)),
            ],
            options={
                'ordering': ('start_date', 'start_time'),
                'verbose_name': 'model:Event',
                'verbose_name_plural': 'models:Event',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hash', models.CharField(unique=True, max_length=40, blank=True)),
                ('file', imagekit.models.fields.ProcessedImageField(upload_to=pagoeta.apps.core.models.get_asset_path,
                                                                    null=True, verbose_name='label:file', blank=True)),
                ('is_featured', models.BooleanField(default=False, verbose_name='label:is_featured')),
                ('is_visible', models.BooleanField(default=True, verbose_name='label:is_visible')),
                ('position', models.PositiveSmallIntegerField(verbose_name='label:position')),
                ('event', models.ForeignKey(related_name='images', blank=True, to='events.Event', null=True)),
            ],
            options={
                'ordering': ('position',),
                'abstract': False,
                'verbose_name': 'model:Image',
                'verbose_name_plural': 'models:Image',
            },
        ),
        migrations.CreateModel(
            name='TargetAge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=100, verbose_name='label:code', db_index=True)),
                ('name', models.CharField(max_length=255, verbose_name='label:name')),
                ('name_eu', models.CharField(max_length=255, null=True, verbose_name='label:name')),
                ('name_es', models.CharField(max_length=255, null=True, verbose_name='label:name')),
                ('name_en', models.CharField(max_length=255, null=True, verbose_name='label:name')),
                ('name_fr', models.CharField(max_length=255, null=True, verbose_name='label:name')),
            ],
            options={
                'ordering': ('id',),
                'verbose_name': 'model:TargetAge',
                'verbose_name_plural': 'models:TargetAge',
            },
        ),
        migrations.CreateModel(
            name='TargetGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=100, verbose_name='label:code', db_index=True)),
                ('name', models.CharField(max_length=255, verbose_name='label:name')),
                ('name_eu', models.CharField(max_length=255, null=True, verbose_name='label:name')),
                ('name_es', models.CharField(max_length=255, null=True, verbose_name='label:name')),
                ('name_en', models.CharField(max_length=255, null=True, verbose_name='label:name')),
                ('name_fr', models.CharField(max_length=255, null=True, verbose_name='label:name')),
            ],
            options={
                'ordering': ('id',),
                'verbose_name': 'model:TargetGroup',
                'verbose_name_plural': 'models:TargetGroup',
            },
        ),
        migrations.AddField(
            model_name='event',
            name='target_age',
            field=models.ForeignKey(related_name='events', verbose_name='model:TargetAge', blank=True,
                                    to='events.TargetAge', null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='target_group',
            field=models.ForeignKey(related_name='events', verbose_name='model:TargetGroup', blank=True,
                                    to='events.TargetGroup', null=True),
        ),
    ]
