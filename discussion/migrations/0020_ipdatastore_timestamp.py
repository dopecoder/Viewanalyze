# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0019_ipdatastore'),
    ]

    operations = [
        migrations.AddField(
            model_name='ipdatastore',
            name='timestamp',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
