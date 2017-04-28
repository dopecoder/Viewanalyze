# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0002_auto_20150723_2026'),
    ]

    operations = [
        migrations.AddField(
            model_name='tempregistration',
            name='email',
            field=models.EmailField(max_length=254, null=True, blank=True),
        ),
    ]
