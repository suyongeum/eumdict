# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-27 04:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_word'),
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'content',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Definitions',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('word', models.CharField(max_length=100)),
                ('wordtype', models.CharField(max_length=100)),
                ('definition', models.TextField()),
            ],
            options={
                'db_table': 'definitions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Line',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('content_id', models.IntegerField()),
                ('line_id', models.IntegerField()),
                ('text', models.TextField()),
                ('difficulty', models.IntegerField()),
            ],
            options={
                'db_table': 'line',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='LineWord',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('content_id', models.IntegerField()),
                ('line_id', models.IntegerField()),
                ('order', models.IntegerField()),
                ('original', models.CharField(max_length=200)),
                ('difficulty', models.IntegerField()),
                ('definition', models.TextField()),
                ('pos', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'line_word',
                'managed': False,
            },
        ),
    ]
