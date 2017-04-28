# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0006_auto_20150722_1223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='analyser',
            name='country',
            field=models.CharField(max_length=40, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='analyser',
            name='dob',
            field=models.DateField(null=True, blank=True),
        ),
    ]
