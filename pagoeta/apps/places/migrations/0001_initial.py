# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import pagoeta.apps.core.models
import imagekit.models.fields


class Migration(migrations.Migration):
    dependencies = [
    ]

    operations = [
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
            ],
            options={
                'ordering': ('position',),
                'abstract': False,
                'verbose_name': 'model:Image',
                'verbose_name_plural': 'models:Image',
            },
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='label:name')),
                ('name_eu', models.CharField(max_length=100, null=True, verbose_name='label:name')),
                ('name_es', models.CharField(max_length=100, null=True, verbose_name='label:name')),
                ('name_en', models.CharField(max_length=100, null=True, verbose_name='label:name')),
                ('name_fr', models.CharField(max_length=100, null=True, verbose_name='label:name')),
                ('description', models.TextField(null=True, verbose_name='label:description', blank=True)),
                ('description_eu', models.TextField(null=True, verbose_name='label:description', blank=True)),
                ('description_es', models.TextField(null=True, verbose_name='label:description', blank=True)),
                ('description_en', models.TextField(null=True, verbose_name='label:description', blank=True)),
                ('description_fr', models.TextField(null=True, verbose_name='label:description', blank=True)),
                ('address', models.CharField(max_length=255, null=True, verbose_name='label:address', blank=True)),
                ('telephone', models.CharField(max_length=32, null=True, verbose_name='label:telephone', blank=True)),
                ('email', models.EmailField(max_length=254, null=True, verbose_name='label:email', blank=True)),
                ('url', models.URLField(null=True, verbose_name='label:url', blank=True)),
                ('price_level', models.SmallIntegerField(null=True, verbose_name='label:price_level', blank=True)),
                ('latitude', models.DecimalField(null=True, verbose_name='label:latitude', max_digits=18,
                                                 decimal_places=12, blank=True)),
                ('longitude', models.DecimalField(null=True, verbose_name='label:longitude', max_digits=18,
                                                  decimal_places=12, blank=True)),
                ('is_visible', models.BooleanField(default=True, verbose_name='label:is_visible')),
            ],
            options={
                'verbose_name': 'model:Place',
                'verbose_name_plural': 'models:Place',
            },
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=32, verbose_name='label:code', db_index=True)),
                ('name', models.CharField(max_length=255, verbose_name='label:name')),
                ('name_eu', models.CharField(max_length=255, null=True, verbose_name='label:name')),
                ('name_es', models.CharField(max_length=255, null=True, verbose_name='label:name')),
                ('name_en', models.CharField(max_length=255, null=True, verbose_name='label:name')),
                ('name_fr', models.CharField(max_length=255, null=True, verbose_name='label:name')),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'model:PlaceType',
                'verbose_name_plural': 'models:PlaceType',
            },
        ),
        migrations.AddField(
            model_name='place',
            name='types',
            field=models.ManyToManyField(related_name='places', verbose_name='models:PlaceType', to='places.Type',
                                         blank=True),
        ),
        migrations.AddField(
            model_name='image',
            name='place',
            field=models.ForeignKey(related_name='images', blank=True, to='places.Place', null=True),
        ),
    ]
