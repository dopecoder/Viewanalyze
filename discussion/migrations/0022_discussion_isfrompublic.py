# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0021_auto_20150812_1851'),
    ]

    operations = [
        migrations.AddField(
            model_name='discussion',
            name='isFromPublic',
            field=models.BooleanField(default=False),
        ),
    ]
