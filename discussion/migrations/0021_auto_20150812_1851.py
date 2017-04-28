# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0020_ipdatastore_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ipdatastore',
            name='ipAddr',
            field=models.CharField(unique=True, max_length=16),
        ),
        migrations.AlterField(
            model_name='ipdatastore',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
