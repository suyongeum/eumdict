# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-03 04:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_auto_20170627_0442'),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name='lineword',
            index_together=set([('content_id', 'line_id')]),
        ),
    ]
